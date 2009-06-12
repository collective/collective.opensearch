import unittest

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

import collective.opensearch

@onsetup
def setup():
    zcml.load_config('configure.zcml', collective.opensearch)

setup()
PloneTestCase.setupPloneSite()

class TestOpenSearchControlPanel(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        portal_setup = self.portal.portal_setup
        # Import the controllpanel step and its dependencies from the default profile.
        self.loginAsPortalOwner()
        portal_setup.runImportStepFromProfile('profile-collective.opensearch:default', 'controlpanel')
        self.logout()

    def test_verify_install(self):
        expected = {
            'title': 'OpenSearch',
            'id': 'OpenSearch',
            'appId': 'OpenSearch',
            'category': 'Products',
            'condition': '',
            'permissions': ('Manage portal',),
            'visible': True}
        portal_controlpanel = self.portal.portal_controlpanel
        # Verify that the configlet was imported via the controlpanel import step.
        opensearch_action = portal_controlpanel.getActionObject('Products/OpenSearch')
        self.failUnless(opensearch_action, "Could not find the configlet in the portal_controlpanel tool.")
        for item in expected:
            self.failUnlessEqual(getattr(opensearch_action, item), expected[item], "The expected value (%s) does not match the actual value (%s)." % (getattr(opensearch_action, item), expected[item]))

    def test_verify_uninstall(self):
        portal_setup = self.portal.portal_setup
        # Import the controlpanel step and its dependencies from the uninstall profile.
        self.loginAsPortalOwner()
        portal_setup.runImportStepFromProfile('profile-collective.opensearch:uninstall', 'uninstall_controlpanel')
        self.logout()
        # Verify the controlpanel step deleted the configlet entry.
        portal_controlpanel = self.portal.portal_controlpanel
        self.failIf(portal_controlpanel.getActionObject('Products/OpenSearch'), "Found the OpenSearch configlet in the portal_controlpanel tool after an uninstall.")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestOpenSearchControlPanel))
    return suite
