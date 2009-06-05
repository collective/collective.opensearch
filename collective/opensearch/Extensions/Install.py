from Products.CMFCore.utils import getToolByName

def install(portal):
    portal_setup = getToolByName(portal, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-collective.opensearch:default')
    return "Ran all import steps."

def uninstall(portal):
    portal_setup = getToolByName(portal, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-collective.opensearch:uninstall')
    return "Ran all uninstall steps."