# SWT-NLP PACKAGE
### PACKAGE INSTALLATION
``` shell
pip install swt-nlp
```

### KEYTERM EXTRACTION
#### OBJECTIVE
* extract new keyterm from corpus

#### DEMO
demo code for keyterm extraction
``` python
from swt.nlp.basis import keyterm_extractor
from tests.keyterm_extraction.test_keyterm_extraction_fit_modules import Mockup

# corpus in format list of plain text
small_content = Mockup.small_corpus()
# small_content[:5] = [
# 'อยากกระโดดน้ำที่แม่น้ำโขง',
# 'แม่น้ำที่จังหวัดกาญจนบุรีนี่สุดยอดมาก',
# 'เหล้ามีหลายยี่ห้อ แสงโสม แม่น้ำโขงหรืออะไรก็มีหมดเลย',
# 'ข้อความนี้เกี่ยวกับชิมช็อปใช้',
# 'รัฐบาลผลักดันชิมช็อปใช้มากขึ้น']

# extract new terms
kt = keyterm_extractor()
# - in case of using a custom tokenizer
# - this example is using word_tokenizer of pythainlp with keep_whitespace=False setting
# custom_tokenizer = lambda t: word_tokenize(t, keep_whitespace=False)  # your own callable tokenizer function 
# kt = keyterm_extractor(tokenizer=custom_tokenizer)
kt.fit(small_content)
new_terms = kt.extract()
# new_terms = ['ชิมช็อปใช้', 'แม่น้ำโขง']
```


### HOW TO BUILD A PACKAGE TO PYPI
prerequisite
``` shell
pip install setuptools wheel tqdm twine
```

build and upload package
``` shell
# preparing tar.gz package 
python setup.py sdist
# uploading package to pypi server
python -m twine upload dist/{package.tar.gz}  --verbose
```

install package
``` shell
# install latest version
pip install swt-nlp --upgrade
# specific version with no cache
pip install swt-nlp==0.0.11  --no-cache-dir
```

install package by wheel
``` shell
# build wheel 
python setup.py bdist_wheel

# install package by wheel 
# use --force-reinstall if needed
pip install dist/{package.whl}
```

