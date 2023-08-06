from swt.nlp.basis import base_processing
from marisa_trie   import Trie
from pythainlp.corpus import thai_words, thai_stopwords


def test_base_processing_default_thai_word_as_pythainlp():
    assert base_processing.THAI_WORDS == thai_words


def test_base_processing_default_thai_stopword_as_pythainlp():
    assert base_processing.THAI_STOPWORDS == thai_stopwords


def test_base_processing_default_preprocessing_with_normal_text_and_digit():
    # normal text with number, uppercase
    text           = 'ข้อความสดทสอบทั่วไป THIS IS a text for demo 01'
    processed_text = base_processing.default_preprocess(text)
    # - check for thai chars
    assert ('ข้อความ' in processed_text) == True
    # - check for eng chars
    assert ('demo'   in processed_text) == True
    # - check for number
    assert ('01'     in processed_text) == True
    # - check for lower case
    assert ('this'   in processed_text) == True
    assert ('THIS'   in processed_text) == False


def test_base_processing_default_preprocessing_with_special_chars():
    """ check lower case, special chars as {@ # . _ >}, shrink whitespace, strip text """
    text           = 'Text me to MUUUSIIIK_NO_REPLY@GMAIL.COM and hashtag >> #demo '
    expected_text  = 'text me to muuusiiik no reply gmail com and hashtag demo'
    processed_text = base_processing.default_preprocess(text)
    assert processed_text == expected_text


def test_base_processing_varidate_trie_vocab_by_given_trie():
    """ make sure the returned type is Trie """
    vocab_list = ['dog', 'cat', 'wilddog', 'catwoman']
    trie_list  = Trie(vocab_list)
    result     = base_processing.validate_trie_vocab(trie_list)
    assert type(result) == Trie
    assert result.keys('cat') == ['cat', 'catwoman']


def test_base_processing_varidate_trie_vocab_by_given_list_of_str():
    """ make sure the returned type is Trie """
    vocab_list     = ['dog', 'cat', '', 'wilddog', 'catwoman']
    processed_list = base_processing.remove_empty_string(vocab_list)
    result         = base_processing.validate_trie_vocab(vocab_list)
    assert type(result) == Trie
    assert result.keys('cat')  == ['cat', 'catwoman']
    assert '' not in processed_list
    assert len(processed_list) == 4



def test_base_processing_default_tokenizer_on_thai():
    text      = 'ช็อปดีมีคืน รอบใหม่ 2565 ลดหย่อนภาษีซื้ออะไรได้บ้าง?'
    tokenizer = base_processing.default_tokenizer()
    result    = tokenizer(text)
    assert ('ช็อป'  in result) == True
    assert ('2565' in result) == True
    assert ('?'    in result) == True

    # preprocessing will remove ? out
    processed_text = base_processing.default_preprocess(text)
    result         = tokenizer(processed_text)
    assert ('ช็อป'  in result) == True
    assert ('2565' in result) == True
    assert ('?'    in result) == False


def test_base_processing_default_tokenizer_on_eng():
    text = 'Can a Chatbot Determine My Diet? Addressing Challenges of Chatbot Application for Meal Recommendation'
    tokenizer = base_processing.default_tokenizer()
    result    = tokenizer(text)
    assert ('Chatbot'    in result) == True
    assert ('Addressing' in result) == True
    assert ('?'          in result) == True

    # preprocessing will remove ? out
    processed_text = base_processing.default_preprocess(text)
    result         = tokenizer(processed_text)
    assert ('chatbot'    in result) == True
    assert ('addressing' in result) == True
    assert ('Chatbot'    in result) == False
    assert ('Addressing' in result) == False
    assert ('?'          in result) == False


def test_base_processing_default_tokenizer_on_digit():
    text = 'ใน Starwars จะมีหุ่นยนต์ชื่อ R2D2 อยู่ 1 ตัวไม่ใช่ 2 ตัว'
    tokenizer = base_processing.default_tokenizer()
    result    = tokenizer(text)
    assert ('Starwars' in result) == True
    assert ('R2D2'     in result) == False
    assert ('หุ่นยนต์'    in result) == True
    assert result.count('2')      == 3
    assert result.count('r')      == 0

    processed_text = base_processing.default_preprocess(text)
    result         = tokenizer(processed_text)
    assert ('starwars' in result) == True
    assert ('r2d2'     in result) == False
    assert ('หุ่นยนต์'    in result) == True
    assert result.count('2')      == 3
    assert result.count('r')      == 1 # from r2d2

# ====================================
# CUSTOM PREPROCESSING AND TOKENIZER
# ====================================
def test_base_preprocessing_custom_preprocess_text_pattern():
    # normal text with number, uppercase
    text           = 'สามารถติดต่อได้ที่เบอร์ 02-345-6789 หรืออีเมล์ SOME_ONE@gmail.com ครับ'
    pattern        = r'[^ก-์a-zA-Z0-9 _.@-]'  # adding _@- in the pattern
    processed_text = base_processing.default_preprocess(text, pattern)
    # - check for thai chars
    assert ('ติดต่อ' in processed_text) == True
    # - check for eng chars
    assert ('@gmail.com' in processed_text) == True
    # - check for number
    assert ('02-345-6789'     in processed_text) == True
    # - check for lower case
    assert ('some_one'   in processed_text) == True
    # - check for special char
    assert ('some_one@gmail.com'   in processed_text) == True


def test_base_processing_custom_tokenizer_on_trie_vocab():
    vocab             = ['ชิมช็อปใช้', 'เราเที่ยวด้วยกัน']
    text              = 'ใช้ร่วมกับชิมช็อปใช้หรือเราเที่ยวด้วยกันได้มั้ย'
    default_tokenizer = base_processing.default_tokenizer()
    custom_tokenizer  = base_processing.default_tokenizer(Trie(vocab))

    default_result = default_tokenizer(text)
    custom_result  = custom_tokenizer(text)

    assert len(default_result) != len(custom_result)
    assert len(custom_result)  == 5


def test_base_processing_custom_tokenizer_on_string_vocab():
    vocab             = ['ชิมช็อปใช้', 'เราเที่ยวด้วยกัน']
    text              = 'ใช้ร่วมกับชิมช็อปใช้หรือเราเที่ยวด้วยกันได้มั้ย'
    default_tokenizer = base_processing.default_tokenizer()
    custom_tokenizer  = base_processing.default_tokenizer(vocab)

    default_result = default_tokenizer(text)
    custom_result  = custom_tokenizer(text)

    assert len(default_result) != len(custom_result)
    assert len(custom_result)  == 5


def test_base_processing_custom_tokenizer_on_keep_whitespace():
    text              = 'ณ ที่นี้ ผองราษำรได้แสดงเจตนารมณ์'
    default_tokenizer = base_processing.default_tokenizer()
    custom_tokenizer  = base_processing.default_tokenizer(keep_whitespace=True)
    default_result    = default_tokenizer(text)
    custom_result     = custom_tokenizer(text)

    assert len(default_result) != len(custom_result)
    assert len(custom_result)  == len(default_result) + 2


def test_base_processing_token_text_with_default_delimiter():
    token             = ['this', 'is', 'a', 'machine learning']
    expected_result   = 'this is a machine_learning'

    assert base_processing.token_text(token) == expected_result


def test_base_processing_token_text_with_custom_delimiter():
    token             = ['this', 'is', 'a', 'machine learning']
    expected_result   = 'this is a machine--learning'

    assert base_processing.token_text(token, delimiter='--') == expected_result
