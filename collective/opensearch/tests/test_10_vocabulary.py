import unittest

from collective.opensearch.browser.vocabulary import searchVocabulary, syndicationVocabulary

class TestSearchVocabulary(unittest.TestCase):

    def test_values(self):
        # get the vocabulary
        vocab = searchVocabulary(object())
        # test the results are as expected
        expected = ['title', 'content']
        for term in vocab:
            self.failUnless(term.value in expected, "the term '%s' is not an expected result." % term.value)
        self.failUnlessEqual(len(vocab), len(expected), "syndicationVocabulary does not have the same number of expected results.")


class TestSyndicationVocabulary(unittest.TestCase):

    def test_values(self):
        # get the vacabulary
        vocab = syndicationVocabulary(object())
        # test the results are as expected
        expected = ['open', 'limited', 'private', 'closed']
        for term in vocab:
            self.failUnless(term.value in expected, "the term '%s' is not an expected result." % term.value)
        self.failUnlessEqual(len(vocab), len(expected), "syndicationVocabulary does not have the same number of expected results.")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSearchVocabulary))
    suite.addTest(unittest.makeSuite(TestSyndicationVocabulary))
    return suite