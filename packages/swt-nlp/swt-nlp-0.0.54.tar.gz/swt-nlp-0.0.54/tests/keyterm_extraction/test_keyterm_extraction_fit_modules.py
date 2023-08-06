import pandas as pd
from   sklearn.feature_extraction.text import CountVectorizer
from   swt.nlp.basis import base_processing, text_processing, keyterm_extractor

# ============
# MOCKUP DATA
# ============
class Mockup:
    def small_corpus(datatype:str='text'):
        content = [
                'อยากกระโดดน้ำที่แม่น้ำโขง',
                'แม่น้ำที่จังหวัดกาญจนบุรีนี่สุดยอดมาก',
                'เหล้ามีหลายยี่ห้อ แสงโสม แม่น้ำโขงหรืออะไรก็มีหมดเลย',
                'ข้อความนี้เกี่ยวกับชิมช็อปใช้',
                'รัฐบาลผลักดันชิมช็อปใช้มากขึ้น',
                'เมื่อก่อนเคยมีนายกทำรายการชิมไปบ่นไปแหละ',
                'พ่อครัวชิมอาหารทุกวัน',
                'สถานที่ท่องเที่ยวริมแม่น้ำเจ้าพระยา',
                'ไปเที่ยวอุทยานแม่น้ำป่าสัก',
                '?', 'ไม่ชอบจริง ๆ ครับ',
                'ไม่ว่าจะมีอะไร ๆ ก็แล้วแต่']
        if   datatype == 'text': return content
        elif datatype == 'df':   return pd.DataFrame({'text': content})
        else:                    return None


# ===================================
# sub module when fit with mode text
# ===================================
def test_keyterm_extraction_checking_adaptive_countvec_is_funciton_properly_in_mode_plain_text_with_default_setting():
    """ plain text mode with default setting (_tokenizer = None)
        plain_text mode --> tokenizer = tp.tokenize()
    """
    demo_text   = 'รีวิว use of IPHONE_14 ได้ มั้ย'
    kt          = keyterm_extractor()
    kt._adaptive_countvectorizer(mode='text')
    params      = kt._countv.get_params()
    tk          = params['tokenizer'] # default tp.tokenize

    tp          = text_processing()
    expected_tk = lambda v: tp.tokenize(v, do_preprocess=None) # do all preprocesses that is set in tp

    # assertation, params equivalant with package S, tokenizer as tp --> lower case enable
    assert tk(demo_text) == expected_tk(demo_text)
    assert 'use'    in tk(demo_text)
    assert 'iphone' in tk(demo_text)
    assert params['max_df'     ] == 1.0
    assert params['min_df'     ] == 1
    assert params['ngram_range'] == (1,3)


def test_keyterm_extraction_checking_adaptive_countvec_is_funciton_properly_in_mode_plain_text_with_custom_cv_without_tokenizer():
    """ plain text mode with custom cv without tokenizer (_tokenizer = None)
        plain_text mode --> tokenizer = tp.tokenize()
    """
    demo_text   = 'รีวิว use of IPHONE_14 ได้ มั้ย'
    cv          = CountVectorizer(ngram_range=(1,4), min_df=2)
    kt          = keyterm_extractor(count_vec=cv)
    #kt._adaptive_countvectorizer(mode='text')
    params      = kt._countv.get_params()
    tk          = params['tokenizer']

    tp          = text_processing()
    expected_tk = lambda v: tp.tokenize(v, do_preprocess=None) # do all preprocesses that is set in tp

    # assertation, params equivalant with package S, tokenizer as tp --> lower case enable
    assert tk(demo_text) == expected_tk(demo_text)
    assert 'use'    in tk(demo_text)
    assert 'iphone' in tk(demo_text)
    assert params['max_df'     ] == 1.0
    assert params['min_df'     ] == 2
    assert params['ngram_range'] == (1,4)


def test_keyterm_extraction_checking_adaptive_countvec_is_funciton_properly_in_mode_plain_text_with_custom_cv_with_tokenizer():
    """ plain text mode with custom cv with tokenizer (_tokenizer != None)
        plain_text mode --> tokenizer = cv.tokenizer
    """
    demo_text   = 'รีวิว use of IPHONE_14 ได้ มั้ย'
    cv          = CountVectorizer(ngram_range=(1,4), min_df=2, tokenizer=lambda t: [it.upper() for it in t.split()])
    kt          = keyterm_extractor(count_vec=cv)
    kt._adaptive_countvectorizer(mode='text')
    params      = kt._countv.get_params()
    tk          = params['tokenizer']

    expected_tk = lambda t: [it.upper() for it in t.split()]

    # assertation, params equivalant with package S, tokenizer is assigned cv.tokenizer
    assert tk(demo_text) == expected_tk(demo_text)
    assert 'USE'       in tk(demo_text)
    assert 'IPHONE_14' in tk(demo_text)
    assert params['max_df'     ] == 1.0
    assert params['min_df'     ] == 2
    assert params['ngram_range'] == (1,4)


# =========================================
# sub module when fit with mode token_text
# =========================================
def test_keyterm_extraction_checking_adaptive_countvec_is_funciton_properly_in_token_text_mode():
    """ in token_text mode, the tokenizer is set as text_processing.tokenize()
    """
    demo_text   = 'รีวิว use of IPHONE_14 ได้ มั้ย'
    kt          = keyterm_extractor.from_package(package='L')
    kt._adaptive_countvectorizer(mode='token_text')
    params      = kt._countv.get_params()

    tk          = params['tokenizer']
    expected_tk = lambda t: t.split()

    # assertation with package L, tokenizer = split, no processing of lower or uppoer text
    assert tk(demo_text) == expected_tk(demo_text)
    assert 'use' in tk(demo_text)
    assert 'IPHONE_14' in tk(demo_text)
    assert params['max_df'     ] == 0.9
    assert params['min_df'     ] == 20
    assert params['ngram_range'] == (1,5)


# ====
# fit :: small corpus
# ====
def test_keyterm_extraction_check_mockup_small_coropus_text_is_correct():
    content    = Mockup.small_corpus()              # plain text
    df         = Mockup.small_corpus(datatype='df') # dataframe
    tp         = text_processing()
    token_text = [tp.tokenize(c, do_postprocess='token_text') for c in content]
    # assertation on plain text
    assert len(content) == 12
    assert '?' in content
    assert 'เมื่อก่อนเคยมีนายกทำรายการชิมไปบ่นไปแหละ' in content
    # assertation on dataframe
    assert len(df)      == 12
    assert (df.text == '?').sum() == 1
    # assertation on token_text
    assert token_text[9] == ''  # sentence no.09 is '' because '?' was removed


def _test_keyterm_extraction_fit_small_corpus_with_token_text_mode_in_string_format():
    content    = Mockup.small_corpus()
    tp         = text_processing()
    token_text = [tp.tokenize(c, do_postprocess='token_text') for c in content]

    kt = keyterm_extractor()
    kt.fit(token_text)
    result = kt.extract(package='S', mode='text', top_n=None)

    assert result == ['ชิมช็อปใช้', 'แม่น้ำโขง']


def _test_keyterm_extraction_fit_small_corpus_with_plain_text_mode_in_string_format():
    content    = Mockup.small_corpus()

    kt = keyterm_extractor()
    kt.fit(content, do_tokenize=True)
    result = kt.extract(package='S', mode='text', top_n=None)

    assert result == ['ชิมช็อปใช้', 'แม่น้ำโขง']



