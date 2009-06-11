from Products.CMFCore.utils import getToolByName

# def install(site):
#     if site.readDataFile('collective.opensearch-install.txt') is None:
#         return


def uninstallControlPanel(site):
    if site.readDataFile('collective.opensearch-controlpanel_uninstall.txt') is None:
        return
    portal_controlpanel = getToolByName(site.getSite(),'portal_controlpanel')
    portal_controlpanel.unregisterConfiglet('OpenSearch')


def uninstallPropertiesTool(site):
    if site.readDataFile('collective.opensearch-propertiestool_uninstall.txt') is None:
        return
    portal_properties = getToolByName(site.getSite(),'portal_properties')
    del portal_properties['opensearch_properties']


# def uninstallActionIcons(site):
#     if site.readDataFile('collective.opensearch-actionicons_uninstall.txt') is None:
#         return
#     portal_properties = getToolByName(site.getSite(),'portal_actions')
