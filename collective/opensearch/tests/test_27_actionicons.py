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

setup()
PloneTestCase.setupPloneSite()

class TestOpenSearchActionIcons(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        portal_setup = self.portal.portal_setup
        # Import the controllpanel step and its dependencies from the default profile.
        self.loginAsPortalOwner()
        portal_setup.runImportStepFromProfile('profile-collective.opensearch:default', 'action-icons')
        self.logout()

    def test_verify_install(self):
        expected = (u'OpenSearch', 0, u'++resource++opensearch.png')
        # Verify the actions-icons step added the action icon entry.
        portal_actionicons = self.portal.portal_actionicons
        info = portal_actionicons.queryActionInfo('controlpanel', 'OpenSearch')
        self.failUnlessEqual(info, expected, "Could not find the OpenSearch action icon in the portal_actionicons tool.")

    def test_verify_uninstall(self):
        # Somehow or other the action icon is magically removed, if an
        # actionicons.xml is not in the uninstall profile.
        # Products.CMFActionIcons 2.1.2 does not support a remove attribute
        # in the actionicons.xml. The profile step will not run without
        # error because the product's exportimport.importActionIconsTool
        # function actually checks for attributes that it does not support
        # (eg. remove).

        portal_setup = self.portal.portal_setup
        # Import the controllpanel step and its dependencies from the default profile.
        self.loginAsPortalOwner()
        portal_setup.runImportStepFromProfile('profile-collective.opensearch:uninstall', 'action-icons')
        self.logout()
        # Verify the actions-icons step deleted the action icon entry.
        portal_actionicons = self.portal.portal_actionicons
        self.failIf(portal_actionicons.queryActionInfo('controlpanel', 'OpenSearch'), "Found the OpenSearch action icon in the portal_actionicons tool after an uninstall.")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestOpenSearchActionIcons))
    return suite
