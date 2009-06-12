import unittest

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase

import collective.opensearch
from collective.opensearch.browser.opensearchprefs import IOpenSearchSettingsForm, OpenSearchControlPanelAdapter

@onsetup
def setup():
    zcml.load_config('configure.zcml', collective.opensearch)
    # ztapi.provideAdapter(IPloneSiteRoot, IOpenSearchSettingsForm, OpenSearchControlPanelAdapter)

setup()
PloneTestCase.setupPloneSite()

class TestOpenSearchAdapter(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        portal_setup = self.portal.portal_setup
        # Import the propertiestool step and its dependencies from the default profile.
        self.loginAsPortalOwner()
        portal_setup.runImportStepFromProfile('profile-collective.opensearch:default', 'propertiestool')
        self.logout()

    def test_verify_install(self):
        expected = {
        "title": 'Plone OpenSearch',
        "description": 'Default description',
        "tags": (),
        "contact": '',
        "longName": '',
        "attribution": '',
        "language": '*',
        "inEncoding": '',
        "outEncoding": '',
        "developer": '',
        "searchMethod": 'title',
        "syndi": 'open',
        "adult": False,
        "allowDiscovery": True,
        "allowRSS": True,
        "allowAtom": True,
        "allowXHTML": True}
        portal_properties = self.portal.portal_properties
        # Verify that the opensearch_properties was imported via the propertiestool import step.
        self.failUnless(portal_properties.get('opensearch_properties'), "Could not find the opensearch_properties in the portal_properties tool.")
        opensearch_properties = portal_properties.get('opensearch_properties')
        # Check that the expected values are in the opensearch_properties object.
        for name in expected:
            expected_value = expected[name]
            actual_value = getattr(opensearch_properties, name)
            self.failUnlessEqual(expected_value, actual_value, "Expected value (%s) does not match the actual value (%s)." % (expected_value, actual_value))

    def test_adapter(self):
        adapter = OpenSearchControlPanelAdapter(self.portal)
        items = {
        "title": "My Site's OpenSearch",
        "description": "My Site's Description",
        "tags": ('kung-pow'),
        "contact": 'me@example.com',
        "longName": 'me',
        "attribution": '',
        # "language": '*',
        # "inEncoding": '',
        # "outEncoding": '',
        "developer": '',
        "syndi": 'limited',
        "adult": True,
        "searchMethod": 'description',
        "allowRSS": True,
        "allowAtom": False,
        "allowXHTML": False,
        "allowDiscovery": True,}
        opensearch_properties = self.portal.portal_properties.opensearch_properties
        # Set 'items' via the adapter.
        for item in items:
            setattr(adapter, item, items[item])
        # Verify the adapter worked as expected.
        for item in items:
            expected_value = items[item]
            actual_value = getattr(opensearch_properties, item)
            self.failUnlessEqual(expected_value, actual_value, "Expected value (%s) does not match the actual value (%s)." % (expected_value, actual_value))

    def test_verify_uninstall(self):
        portal_setup = self.portal.portal_setup
        # Import the propertiestool step and its dependencies from the uninstall profile.
        self.loginAsPortalOwner()
        portal_setup.runImportStepFromProfile('profile-collective.opensearch:uninstall', 'uninstall_propertiestool')
        self.logout()
        # Verify the propertiestool step deleted the opensearch_properties object.
        portal_properties = self.portal.portal_properties
        self.failIf(portal_properties.get('opensearch_properties'), "Found the opensearch_properties in the portal_properties tool after an uninstall.")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestOpenSearchAdapter))
    return suite
