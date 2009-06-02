from zope.schema.vocabulary import SimpleVocabulary

def syndicationVocabulary(context):
    subjects = ('open',
                'limited',
                'private',
                'closed',
    )
    return SimpleVocabulary.fromValues(subjects)


def searchVocabulary(context):
    searchType = ('title',
                'content',
    )
    return SimpleVocabulary.fromValues(searchType)    
