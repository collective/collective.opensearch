import logging
# The profile id of your package:
PROFILE_ID = 'profile-collective.opensearch:default'
from Products.CMFCore.utils import getToolByName

def update_registry(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.opensearch')
        logger.info("import regisitry setting")
    setup = getToolByName(context, 'portal_setup')
    #setup.runImportStepFromProfile(PROFILE_ID, 'portal_registry')



def import_various(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('collective.opensearch-default.txt') is None:
        return
    logger = context.getLogger('collective.opensearch')
    site = context.getSite()
    pass
