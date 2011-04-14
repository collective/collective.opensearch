# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

class IndexesVocabulary(object):
    """Vocabulary factory for indexes of a cloud.
    """
    implements( IVocabularyFactory )

    def __call__(self, context):
        registry = getUtility(IRegistry)
        portal_catalog = getToolByName(registry.getParentNode(), 'portal_catalog')
        remove_indexes = ['allowedRolesAndUsers','getRawRelatedItems','object_provides']
        indexes = [x for x in portal_catalog.Indexes
                   if portal_catalog.Indexes[x].meta_type=='KeywordIndex'
                   and not x in remove_indexes]
        terms = [SimpleTerm(index,index) for index in indexes]
        return SimpleVocabulary(terms)

IndexesVocabularyFactory = IndexesVocabulary()
