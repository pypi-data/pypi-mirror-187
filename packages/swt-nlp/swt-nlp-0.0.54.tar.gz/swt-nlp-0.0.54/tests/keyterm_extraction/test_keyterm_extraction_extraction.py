from swt.nlp.basis import text_processing, keyterm_extractor
from sklearn.feature_extraction.text import CountVectorizer

class MockEnv:
    def small_corpus():
        return []


# ===============
# FIT VARIATIONS
# ===============
def test_keyterm_extractor_fit_plain_text():
    corpus = MockEnv.small_corpus()


def test_keyterm_extractor_fit_token_text():
    ...


# ===========
# EXTRACTION
# ===========
def _test_keyterm_extractor_extract_small_data():
    ...


def _test_keyterm_extractor_extract_large_data():
    ...

