import muuusiiik.util as msk
from   swt.nlp.basis import base_processing, text_processing
from   pytest import raises

class MockEnv:
    env_path    = 'tests/_data'
    f_configure = f'{env_path}/system.conf'

    def create_env():
        msk.data.make_path(MockEnv.f_configure)

    def remove_env():
        msk.data.rm(MockEnv.env_path)

    def create_configure(conf):
        msk.configure.save(conf, MockEnv.f_configure)

    def create_contents(contents):
        for k, v in contents.items():
            f = f'{MockEnv.env_path}/{k}'
            msk.data.save(v, f)



# ================================
# LOAD VOCAB FROM VARIOUS SOURCES
# ================================
def test_load_custom_vocab_list_from_module_init():
    vocab_list = ['ชิมช็อปใช้', 'เราเที่ยวด้วยกัน']
    text       = 'ขอโปรชิมช็อปใช้กับเราเที่ยวด้วยกันหน่อย'
    # create tokenizer outside the class
    tokenizer  = base_processing.default_tokenizer(vocab_list)
    # init the class with a tokenizer
    tp         = text_processing(tokenizer=tokenizer)
    result     = tp.tokenize(text)

    assert len(result) == 5
    assert result      == ['ขอโปร', 'ชิมช็อปใช้', 'กับ', 'เราเที่ยวด้วยกัน', 'หน่อย']


def test_load_custom_vocab_list_from_module_vocab_list():
    vocab_list = ['ชิมช็อปใช้', 'เราเที่ยวด้วยกัน']
    text       = 'ขอโปรชิมช็อปใช้กับเราเที่ยวด้วยกันหน่อย'
    # init the class with a tokenizer
    tp         = text_processing.from_vocab_list(vocab_list=vocab_list)
    result     = tp.tokenize(text)

    assert len(result) == 5
    assert result      == ['ขอโปร', 'ชิมช็อปใช้', 'กับ', 'เราเที่ยวด้วยกัน', 'หน่อย']


def test_load_custom_vocab_list_from_module_vocab_list_with_empty_string():
    vocab_list = ['ชิมช็อปใช้', '', 'เราเที่ยวด้วยกัน']
    text       = 'ขอโปรชิมช็อปใช้กับเราเที่ยวด้วยกันหน่อย'
    # init the class with a tokenizer
    tp         = text_processing.from_vocab_list(vocab_list=vocab_list)
    result     = tp.tokenize(text)

    assert len(result) == 5
    assert result      == ['ขอโปร', 'ชิมช็อปใช้', 'กับ', 'เราเที่ยวด้วยกัน', 'หน่อย']


def test_load_custom_vocab_list_from_module_load():
    vocab_list = ['ชิมช็อปใช้', 'เราเที่ยวด้วยกัน']
    text       = 'ขอโปรชิมช็อปใช้กับเราเที่ยวด้วยกันหน่อย'

    # DEFAULT SETTING
    tp             = text_processing()
    default_result = tp.tokenize(text)
    # CUSTOM SETTING
    # - create tokenizer outside the class
    tokenizer      = base_processing.default_tokenizer(vocab_list)
    # - load the tokenizer to the class
    tp.load(tokenizer=tokenizer)
    result         = tp.tokenize(text)

    assert len(result)         == 5
    assert len(default_result) != len(result)
    assert default_result      == ['ขอ', 'โปร', 'ชิม', 'ช็อป', 'ใช้กับ', 'เรา', 'เที่ยว', 'ด้วยกัน', 'หน่อย']
    assert result              == ['ขอโปร', 'ชิมช็อปใช้', 'กับ', 'เราเที่ยวด้วยกัน', 'หน่อย']


def test_load_custom_vocab_from_configure_file():
    text     = 'ขอโปรชิมช็อปใช้กับเราเที่ยวด้วยกันหน่อย'
    # generate configure with 2 vocab files
    contents = {
                'file01.vocab': ['ชิมช็อปใช้', 'เราเที่ยวด้วยกัน'],
                'file02.vocab': ['แมงกะพรุนไฟ', 'ตัวเงินตัวทอง']
               }
    configure = {'vocab': [f'{MockEnv.env_path}/{k}' for k, v in contents.items()]}
    # - create configure file
    MockEnv.create_configure(configure)
    # - create vocab files
    MockEnv.create_contents(contents)

    # LOAD CUSTOM VOCAB FROM CONFIGURE
    f_configure = MockEnv.f_configure
    tp          = text_processing.from_configure(f_configure)
    result      = tp.tokenize(text)
    # assertation
    assert len(result)         == 5
    assert result              == ['ขอโปร', 'ชิมช็อปใช้', 'กับ', 'เราเที่ยวด้วยกัน', 'หน่อย']
    # reset env
    MockEnv.remove_env()


def test_load_custom_vocab_from_configure_file_with_custom_tag():
    text     = 'ขอโปรชิมช็อปใช้กับเราเที่ยวด้วยกันหน่อย'
    # generate configure with 2 vocab files
    contents = {
                'file01.vocab': ['ชิมช็อปใช้', 'เราเที่ยวด้วยกัน'],
                'file02.vocab': ['แมงกะพรุนไฟ', 'ตัวเงินตัวทอง']
               }
    tag       = 'custom_vocab'
    configure = {tag: [f'{MockEnv.env_path}/{k}' for k, v in contents.items()]}
    # - create configure file
    MockEnv.create_configure(configure)
    # - create vocab files
    MockEnv.create_contents(contents)

    # LOAD CUSTOM VOCAB FROM CONFIGURE
    f_configure = MockEnv.f_configure
    tp          = text_processing.from_configure(f_configure, tag=tag)  # load vocab list with using custom tag
    result      = tp.tokenize(text)
    # assertation
    assert len(result)         == 5
    assert result              == ['ขอโปร', 'ชิมช็อปใช้', 'กับ', 'เราเที่ยวด้วยกัน', 'หน่อย']
    # reset env
    MockEnv.remove_env()


def test_load_custom_vocab_from_non_existing_configure_file():
    f_configure = 'tests/_data/not_existing_file.conf'
    with raises(FileNotFoundError):
        tp = text_processing.from_configure(f_configure)


def test_load_custom_vocab_from_none_configure_file():
    f_configure = None
    with raises(TypeError):
        tp = text_processing.from_configure(f_configure)

