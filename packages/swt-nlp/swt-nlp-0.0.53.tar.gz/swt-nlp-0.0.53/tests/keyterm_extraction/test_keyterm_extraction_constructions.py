from swt.nlp.basis import text_processing, keyterm_extractor
from sklearn.feature_extraction.text import CountVectorizer
from pytest import raises

# =============
# CONSTRUCTION
# =============
def test_keyterm_extractor_default_construction_with_tokenizer_and_counter_vectorizer():
    """ full customization
        * tokenizer (vocab list, preprocess, postprocess)
        * counter_vectorizer (ngram, min_df, max_df, stopwords)
        * NOTHING -> tokenizer = split
    """
    vocab_list = ['หมา', 'แมว']
    text       = 'เลี้ยงลูกหมาเป็นสิบตัว'
    tp = text_processing.from_vocab_list(vocab_list=vocab_list)
    cv = CountVectorizer(ngram_range=(1,4), min_df=2)
    kt = keyterm_extractor(tp=tp, count_vec=cv)

    params = kt._countv.get_params()

    assert kt._package == 'C'
    assert params['ngram_range'] == (1,4)
    assert params['min_df'     ] == 2
    assert params['tokenizer']   != None  # cv oritignally does not assign tokenizer, it will be set as default pythainlp tokenizer
    assert len(params['tokenizer'](text)) == 3
    assert len(kt._tp.tokenize(text))     == 3


def test_keyterm_extractor_with_default_without_setting():
    """ without setting, 
        tp = default_tokenizer
        cv = package S
    """
    kt     = keyterm_extractor()
    tp     = text_processing()
    params = kt._countv.get_params()
    assert kt._package == 'S'
    assert params['ngram_range'] == (1,3)
    assert params['min_df']      == 1
    assert params['tokenizer']   != None  # cv oritignally does not assign tokenizer, it will be set as default pythainlp tokenizer
    # tokenzer work the same flow as default tokenizer
    text   = 'สวัสดีครับร้านนี้ใช้ชิมช็อปใช้ได้มั้ย'
    assert kt._tp.tokenize(text)  == tp.tokenize(text)
    assert len(tp.tokenize(text)) >  1 # tokenize() is working


def test_keyterm_extractor_with_package_S_setting():
    """ without setting, 
        tp = default_tokenizer
        cv = package S
    """
    kt     = keyterm_extractor.from_package(package='S')
    tp     = text_processing()
    params = kt._countv.get_params()
    assert kt._package == 'S'
    assert params['ngram_range'] == (1,3)
    assert params['max_df']      == 1.0
    assert params['min_df']      == 1
    assert params['tokenizer']   != None
    # tokenzer work the same flow as default tokenizer
    text   = 'สวัสดีครับร้านนี้ใช้ชิมช็อปใช้ได้มั้ย'
    assert kt._tp.tokenize(text)  == tp.tokenize(text)
    assert len(tp.tokenize(text)) >  1  # tokenize() is working


def test_keyterm_extractor_with_package_L_setting():
    """ without setting, 
        tp = default_tokenizer
        cv = package L
    """
    kt     = keyterm_extractor.from_package(package='L')
    tp     = text_processing()
    params = kt._countv.get_params()
    assert kt._package == 'L'
    assert params['ngram_range'] == (1,5)
    assert params['max_df']      == 0.9
    assert params['min_df']      == 20
    assert params['tokenizer']   != None
    # tokenzer work the same flow as default tokenizer
    text   = 'สวัสดีครับร้านนี้ใช้ชิมช็อปใช้ได้มั้ย'
    assert kt._tp.tokenize(text)  == tp.tokenize(text)
    assert len(tp.tokenize(text)) >  1  # tokenize() is working


def test_keyterm_extractor_with_non_existing_package():
    """ without setting, 
        tp = default_tokenizer
        cv = package XX
    """
    with raises(ValueError):
        kt     = keyterm_extractor.from_package(package='XX')
