from   swt.nlp.basis import text_processing
import re

# =========================================
# FOCUSING ON DEFAULT TOKENIZING PROCESSES 
# =========================================
def test_default_text_processing():
    text = 'สวัสดีวันจันทร์ MONDAY อังคาร '
    tp   = text_processing()

    # default structure
    assert len(tp._preprocesses)  == 1
    assert 'default' in tp._preprocesses
    assert len(tp._postprocesses) == 1
    assert 'token_text' in tp._postprocesses
    # result with different setting
    expected = ['สวัสดี', 'วัน', 'จันทร์', 'monday', 'อังคาร']
    result   = tp.tokenize(text)
    assert result == expected
    # result with NON preprocess
    expected = ['สวัสดี', 'วัน', 'จันทร์', 'monday', 'อังคาร']
    result   = tp.tokenize(text, do_preprocess=None)
    assert result == expected
    # result with {token_text} postprocess
    expected = 'สวัสดี วัน จันทร์ monday อังคาร'
    result   = tp.tokenize(text, do_postprocess='token_text')
    assert result == expected


def test_default_preprocesses():
    text = 'สวัสดีวันจันทร์ MONDAY อังคาร '
    tp   = text_processing()

    processed_text = tp.preprocesses(text)
    assert len(tp._preprocesses) == 1
    assert 'default' in tp._preprocesses
    assert processed_text == 'สวัสดีวันจันทร์ monday อังคาร'


def test_default_tokenizer():
    text       = 'สวัสดีวันจันทร์'
    tp         = text_processing()
    
    result     = tp._tokenizer(text)
    assert len(result) == 3
    assert result      == ['สวัสดี', 'วัน', 'จันทร์']


def test_default_postprocesses():
    """ default postprocess is do nothing since param process = []
    """
    token      = ['สวัสดี', 'วัน', 'จันทร์']
    tp         = text_processing()
    
    result     = tp.postprocesses(token)
    assert len(tp._postprocesses) == 1
    assert 'token_text' in tp._postprocesses
    assert len(result)            == 3
    assert result                 == ['สวัสดี', 'วัน', 'จันทร์']


def test_text_processing_tokenize_with_defult_processes_combined():
    text   = 'สวัสดีวันจันทร์ MONDAY อังคาร '
    tp     = text_processing()

    result = tp.tokenize(text)
    assert result == ['สวัสดี', 'วัน', 'จันทร์', 'monday', 'อังคาร']


def test_text_processing_tokenize_with_defult_processes_combined_with_postprocess_is_token_text():
    text   = 'สวัสดีวันจันทร์ MONDAY อังคาร '
    tp     = text_processing()

    result = tp.tokenize(text, do_postprocess='token_text')
    assert result == 'สวัสดี วัน จันทร์ monday อังคาร'


# =========================================
# FOCUSING ON CUSTOM TOKENIZING PROCESSES 
# =========================================
def test_preprocessing_text_custom_preprocess_with_lower_case():
    text   = 'สวัสดีวันจันทร์ MONDAY อังคาร '
    pre    = lambda t: t.lower()

    tp     = text_processing(pre)
    result = tp.preprocesses(text)
    assert result == 'สวัสดีวันจันทร์ monday อังคาร '


def test_preprocessing_text_custom_preprocess_with_adding_remove_special_chars():
    # prebuilt with lower_case preprocessing
    text   = 'เมล์กลับมาที่ SOME_ONE-NO-REPLY@EMAIL.COM #TESTING '
    preset = lambda t: t.lower()
    tp     = text_processing(preset)
    # adding remove_special_char preprocessing
    chars  = r'[^ก-์a-zA-Z0-9 @#-._]'
    remove = {'remove': lambda t: re.sub(chars, '', t)}
    tp.add_preprocess(remove)
    # processing
    result = tp.preprocesses(text)
    # assertation
    assert len(tp._preprocesses) == 2
    assert 'custom_00' in tp._preprocesses
    assert 'remove'    in tp._preprocesses
    assert result == 'เมล์กลับมาที่ some_one-no-reply@email.com #testing '


def test_text_processing_custom_postprocess():
    text   = 'สวัสดีวันจันทร์ MONDAY อังคาร '
    # adding 2 post processes
    post   = [lambda arr: '_'.join(arr), lambda t: f'hello_{t}']
    # init class
    tp     = text_processing(postprocesses=post)
    # tokenize with preprocess and postprocess
    result = tp.tokenize(text, do_postprocess=None)
    # assertation
    assert result == 'hello_สวัสดี_วัน_จันทร์_monday_อังคาร'

def test_disable_postprocess_in_tokenize_module_by_setting_flag():
    text   = 'สวัสดีวันจันทร์ MONDAY อังคาร '
    # adding 2 post processes
    post   = [lambda arr: '_'.join(arr), lambda t: f'hello_{t}']
    # init class
    tp     = text_processing(postprocesses=post)
    # tokenize with preprocess and postprocess
    result = tp.tokenize(text, do_postprocess=[])
    # assertation
    assert result == ['สวัสดี', 'วัน', 'จันทร์', 'monday', 'อังคาร']


def test_text_processing_correctly_tokenize_when_assigned_mixed_processes():
    preprocess  = {'lower': lambda t: t.lower(), 'upper': lambda t: t.upper()}
    postprocess = lambda t: t
    text        = 'apple manGO BANANA'
    tp          = text_processing(preprocesses=preprocess)
    tp.add_postprocess(postprocess)

    tlower      = 'apple mango banana'
    tupper      = 'APPLE MANGO BANANA'

    assert len(tp._preprocesses)  == 2
    assert len(tp._postprocesses) == 2
    assert 'token_text' in tp._postprocesses
    assert 'custom_00'  in tp._postprocesses

    assert tp.tokenize(text, do_preprocess='lower')      == ['apple', 'mango', 'banana']
    assert tp.tokenize(text, do_preprocess='upper')      == ['APPLE', 'MANGO', 'BANANA']
    assert tp.tokenize(text)                             == ['APPLE', 'MANGO', 'BANANA']
    assert tp.tokenize(text, do_preprocess=[])           == ['apple', 'manGO', 'BANANA']
    assert tp.tokenize(text, do_postprocess=None)        == 'APPLE MANGO BANANA'
    assert tp.tokenize(text, do_preprocess=['lower'], do_postprocess=['custom_00']) == ['apple', 'mango', 'banana']

