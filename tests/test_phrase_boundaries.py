import unittest
from app.analyzer import matches_keyword
class PhraseBoundaryTests(unittest.TestCase):
    def test_partial_words_do_not_invent_incidents(self):
        for message,keyword in [('timeoutless operation','timeout'),('disk fullness metric','disk full'),('crash looping documentation','crash loop'),('oomkilledness','oomkilled')]:
            self.assertFalse(matches_keyword(message,keyword))
    def test_punctuation_and_timeout_plural_are_supported(self):
        for message,keyword in [('request timeouts.','timeout'),('error: disk full!','disk full'),('pod=oomkilled','oomkilled')]:
            self.assertTrue(matches_keyword(message,keyword))
