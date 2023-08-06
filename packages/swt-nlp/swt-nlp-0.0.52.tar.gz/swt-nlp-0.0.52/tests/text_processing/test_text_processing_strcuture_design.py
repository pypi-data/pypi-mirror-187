from swt.nlp.basis import base_processing, text_processing

def test_text_processing_default_setting():
    tp = text_processing()
    assert len(tp._preprocesses)  == 1
    assert len(tp._postprocesses) == 1
    assert 'default'    in tp._preprocesses
    assert 'token_text' in tp._postprocesses


def test_text_processing_custom_setting():
    # no preprocesses
    tp = text_processing(preprocesses=[])
    assert len(tp._preprocesses)  == 0
    assert len(tp._postprocesses) == 1

    # stacked preprocess
    tp = text_processing(preprocesses=[lambda t: t.lower(), lambda t: t.strip()])
    tp.add_preprocess({'demo_pre': lambda: x})
    tp.add_postprocess({'demo': lambda x: x})
    assert len(tp._preprocesses)  == 3
    assert len(tp._postprocesses) == 2
    assert 'custom_00'  in tp._preprocesses
    assert 'custom_01'  in tp._preprocesses
    assert 'demo_pre'   in tp._preprocesses
    assert 'token_text' in tp._postprocesses
    assert 'demo'       in tp._postprocesses


def test_text_processing_assigned_dict_process():
    preprocess  = {'lower': lambda t: t.lower(), 'upper': lambda t: t.upper()}
    postprocess = {'nothing': lambda t: t}
    tp          = text_processing(preprocesses=preprocess, postprocesses=postprocess)

    assert len(tp._preprocesses)  == 2
    assert 'lower'   in tp._preprocesses
    assert 'upper'   in tp._preprocesses
    assert len(tp._postprocesses) == 1
    assert 'nothing' in tp._postprocesses


def test_text_processing_assigned_callable_processes_should_create_default_keys():
    preprocess  = [lambda t: t.lower(), lambda t: t.upper()]
    postprocess = lambda t: t
    tp          = text_processing(preprocesses=preprocess, postprocesses=postprocess)

    assert len(tp._preprocesses)  == 2
    assert 'custom_00' in tp._preprocesses
    assert 'custom_01' in tp._preprocesses
    assert len(tp._postprocesses) == 1
    assert 'custom_00' in tp._postprocesses


