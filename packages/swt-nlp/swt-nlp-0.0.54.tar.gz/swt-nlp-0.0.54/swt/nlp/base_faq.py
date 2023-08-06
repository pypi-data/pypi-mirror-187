import muuusiiik.util as msk
import fasttext

from   sklearn.feature_extraction.text import TfidfVectorizer
from   sklearn.metrics.pairwise import linear_kernel
from   sklearn.exceptions import NotFittedError

class ClassifierModuleNotFound(Exception): ...
class SearchModuleNotFound(Exception): ...

class base_faq:
    def __init__(self, verbose:bool=False):
        # tokenizer
        self._tp            = None
        # faq related params
        self._faq_configure = None
        self._faq           = None
        self._tfidf         = None
        self._model         = None
        self._faq_matrix    = None
        self._field_query   = None
        self._field_answer  = None
        self._fallback      = None
        # misc
        self._verbose = verbose
        self._info    = {}
        self._status  = {}
        self._L       = None  # log

    ###################
    #       UTIL
    ###################
    def _file_faq_handler(self, key_name, format_name):
        try:
            return self._faq_configure[key_name]
        except KeyError as e:
            f_faq = self._faq_configure['faq']
            core_name = '.'.join(f_faq.split('.')[:-1])
            f_out = core_name + format_name
            return f_out
        except Exception as e:
            raise e

    ###################
    #   SETTER PARAMS
    ###################
    def set(self, faq_configure=None, tokenizer=None, faq=None, model=None, tfidf=None):
        """ setter
        """
        if faq_configure: self._faq_configure = faq_configure
        if tokenizer:     self._tp    = tokenizer
        if faq:           self._faq   = faq
        if model:         self._model = model
        if tfidf:         self._tfidf = tfidf


    def parse(self, **kwargs):
        """ parse content from input dictionary
        """
        

