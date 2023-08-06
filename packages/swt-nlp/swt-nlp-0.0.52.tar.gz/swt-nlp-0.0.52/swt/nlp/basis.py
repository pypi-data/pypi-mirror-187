import pandas as pd
import muuusiiik.util as msk
import re
from   itertools import product
from   marisa_trie import Trie
from   pythainlp.tokenize import word_tokenize
from   pythainlp.corpus import thai_words, thai_stopwords
from   sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# ==================
# EXCEPTION CLASSES
# ==================
class TokenizerNotFoundError(Exception):
    pass

        



# ==================
# CORE CLASSES
# ==================
class BTrie:
    def __init__(self, terms=None):
        self.load(terms)

    def backward(term):
        return term[::-1] if term else None

    def load(self, terms=None):
        """ terms are list of words """
        self.ftrie = Trie(terms)
        rv_terms   = [BTrie.backward(t) for t in terms] if terms else None
        self.btrie = Trie(rv_terms)


    def bkeys(self, term=None):
        rv_term    = BTrie.backward(term)
        rv_keys    = self.btrie.keys(rv_term)
        return [BTrie.backward(rk) for rk in rv_keys]


    def keys(self, term=None, mode='fwd'):
        """ mode = [fwd, bwd, duo] """
        if mode == 'fwd':
            return self.ftrie.keys(term)
        elif mode == 'bwd':
            return self.btrie.keys(term)
        else:
            return self.ftrie.keys(term), self.bkeys(term)


    def bprefixes(self, term=None):
        rv_term    = BTrie.backward(term)
        rv_keys    = self.btrie.prefixes(rv_term)
        return [BTrie.backward(rk) for rk in rv_keys]

    def prefixes(self, term=None, mode='fwd'):
        """ mode = [fwd, bwd, duo] """
        if mode == 'fwd':
            return self.ftrie.prefixes(term)
        elif mode == 'bwd':
            return self.btrie.bprefixes(term)
        else:
            return self.ftrie.prefixes(term), self.bprefixes(term)





class base_processing:
    TEXT_PATTERN   = r'[^ก-์a-zA-Z0-9 ]'
    THAI_WORDS     = thai_words
    THAI_STOPWORDS = thai_stopwords

    # FOR FORMER USEAGE OF THIS MODULE
    def preprocess(text, text_pattern=None) -> str:
        """ set preprocess method such as lower, filter some char out
        """
        try:
            text_pattern = text_pattern if text_pattern else base_processing.TEXT_PATTERN
            text = text.lower()
            text = re.sub(text_pattern, ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            return text 
        
        except Exception as e:
            print(f' > preprocessing() error: {str(e)}')
            print(f'   text: {text}')
            return ''


    def remove_empty_string(vocab_list):
        try:
            # unique vocab_list
            vocab_list = list(set(vocab_list))
            # remove empty string
            idx = vocab_list.index('')
            vocab_list.pop(idx)
            return vocab_list
        except:
            return vocab_list


    def validate_trie_vocab(trie_vocab:Trie=None):
        """ make sure the given trie_vovab is Trie type not list of string
            it trie_vocab is None, the default THAI_WORDS() return
        """
        if trie_vocab is None: trie_vocab = Trie(base_processing.THAI_WORDS())
        if type(trie_vocab) == list: 
            trie_vocab = Trie(base_processing.remove_empty_string(trie_vocab))
        return trie_vocab


    # THE SAME AS PREPROCESS WITH COMMENT
    def default_preprocess(text, text_pattern=None) -> str:
        """ set preprocess method such as lower, filter some char out
        """
        try:
            # set pattern
            text_pattern = text_pattern if text_pattern else base_processing.TEXT_PATTERN
            # lower case
            text = text.lower()
            # replace matched pattern with space
            text = re.sub(text_pattern, ' ', text)
            # shrink spaces
            text = re.sub(r'\s+', ' ', text)
            # strip text
            text = text.strip()
            return text

        except Exception as e:
            print(f' > preprocessing() error: {str(e)}')
            print(f'   text: {text}')
            return ''


    def default_tokenizer(trie_vocab:Trie=None, keep_whitespace:bool=False):
        """ assign default tokenizer using custom dict
        """
        trie_vocab = base_processing.validate_trie_vocab(trie_vocab)
        tokenizer  = lambda text: word_tokenize(text, keep_whitespace=keep_whitespace, custom_dict=trie_vocab)
        return tokenizer


    def token_text(token, delimiter:str='_'):
        """ input as list of string and return a string that replace {space} in each token with {delimiter}
            e.g., token is ['this', 'is', 'machine learning']
            output is 'this is machine_learning'
        """
        return ' '.join([delimiter.join(t for t in tk.split()) for tk in token])



class text_processing:
    """ objective: doing these followings
        * preprocessing  - e.g., lower case, remove special chars, normalize term, etc
        * tokenizing     - segmentation
        * postprocessing - e.g., weighting, combine tokens, etc
    """
    def __init__(self, preprocesses=None, tokenizer=None, postprocesses=None, verbose:bool=False, **kwargs):
        self._verbose = verbose
        self.reset()
        self.load(preprocesses, tokenizer, postprocesses, **kwargs)


    def reset(self):
        self._preprocesses   = {}
        self._tokenizer      = None
        self._postprocesses  = {}


    # ref https://tutorial.eyehunts.com/python/constructor-overloading-in-python-example-code/
    @classmethod
    def from_configure(cls, f_configure, tag:str='vocab', verbose:bool=True):
        """ load a configure file in yaml format. this module will crawling content in the files under given tag {tag} as vocab set
            * f_configure - file name of configure
            * tag         - tag that contains filename list, each filename contains vocab set
        """
        try:
            # load configure
            configure = msk.configure_loader(f_configure)
            # handling tokenizer
            f_vocab_list    = configure.get(tag)
            vocab_list      = msk.data.load_file_list(f_vocab_list, verbose=verbose)
            tokenizer       = base_processing.default_tokenizer(vocab_list)
            return cls(tokenizer=tokenizer, verbose=verbose)

        except FileNotFoundError as e:
            raise e

        except TypeError as e:
            raise e

        except Exception as e:
            raise e


    @classmethod
    def from_vocab_list(cls, preprocesses=None, vocab_list:list=None, postprocesses=None, verbose:bool=False):
        # HANDLE TOKENIZER
        trie_vocab = base_processing.validate_trie_vocab(vocab_list)
        tokenizer  = base_processing.default_tokenizer(trie_vocab)
        return cls(preprocesses=preprocesses, tokenizer=tokenizer, postprocesses=postprocesses, verbose=verbose)



    def _validate_process(self, process, default_process):
        """ validate if the given process (either preprocess or postprocess) is assigned as dict format
            return default_preocess if None is given
            return {} if {empty list} or {empty dict} is given since the user intentionally assigned empty value
            return {'custom_xx': fnc, ... } if list of callable fnc given
        """
        if process is None: return default_process
        if type(process) is dict: return process
        if callable(process): process = [process]
        if type(process) is list: return {f'custom_{idx:02}': p for idx, p in enumerate(process) if callable(p)}
        return default_process


    def _validate_tokenizer(self, process, default_process):
        """ validate if the tokenizer process is callable otherwise assigning the default one
        """
        # case of something is assigned
        if callable(process): return process
        # case of None or [] is assigned
        else: return default_process if process is None else None
        

    def load(self, preprocesses=None, tokenizer=None, postprocesses=None, **kwargs):
        """ assign preprocess, tokenizer and postprocess
        """
        # validate content
        tokenizer = self._validate_tokenizer(tokenizer, base_processing.default_tokenizer())

        # ASSIGN PREPROCESS
        self.add_preprocess(preprocesses)

        # ASSIGN TOKENIZER
        if tokenizer: self._tokenizer = tokenizer

        # ASSIGN POSTPROCESS
        self.add_postprocess(postprocesses)



    # ---------------------------------
    # text_processing: adding processes
    # ---------------------------------
    def add_preprocess(self, preprocesses):
        """ preprocesses should be dict or list or None
            None --> add default preprocess
            dict --> adding assgined preprocess
            list --> check if each process is callable or not than assigned default key as {custom_xx}
        """
        preprocesses  = self._validate_process(preprocesses,  {'default': base_processing.default_preprocess})
        self._preprocesses.update(preprocesses)


    def add_postprocess(self, postprocesses):
        """ postprocesses should be dict or list or None
            None --> add default postprocess
            dict --> adding assgined postprocess
            list --> check if each process is callable or not than assigned default key as {custom_xx}
        """
        postprocesses  = self._validate_process(postprocesses,  {'token_text': base_processing.token_text})
        self._postprocesses.update(postprocesses)


    # ------------------------
    # text_processing: actions 
    # ------------------------
    def preprocesses(self, text:str, process=None) -> str:
        """ do preprocess text
            input is string
            output is string
            process is a parameter that selecting modules for preprocessing
            - None - apply all prepeocess modules
            - str  - specific single module name
            - list - do processing modules as given names
            - do nothing if the name does not match
        """
        try:
            targets = process if type(process) is list else list(self._preprocesses.keys()) if process is None else [process]
            for idx, target in enumerate(targets):
                if target in self._preprocesses:
                    text = self._preprocesses[target](text)

            return text


        except Exception as e:
            if self._verbose: print(f'> preprocess() no.{idx} with "{process}" error - {type(e)} - {str(e)}')
            raise e


    def postprocesses(self, tokens, process=[]):
        """ do postprocess text
            input is token
            output is up-to the process moduels
            process is a parameter that selecting modules for preprocessing
            - None - apply all prepeocess modules
            - str  - specific single module name
            - list - do processing modules as given names
            - do nothing if the name does not match
        """
        try:
            targets = process if type(process) is list else list(self._postprocesses.keys()) if process is None else [process]
            for idx, target in enumerate(targets):
                if target in self._postprocesses:
                    tokens = self._postprocesses[target](tokens)

            return tokens

        except Exception as e:
            if self._verbose: print(f'> postprocess() no.{idx} with "{postprocess}" error - {type(e)} - {str(e)}')
            raise e

        
    def tokenize(self, text:str, **kwargs):
        result = text
        # do preprocessing
        do_preprocess = kwargs.get('do_preprocess', None)
        result = self.preprocesses(result, do_preprocess)
        # do tokenizing
        result = self._tokenizer(result)
        # do postprocessing
        do_postprocess = kwargs.get('do_postprocess', [])
        result = self.postprocesses(result, do_postprocess)
        return result





class _text_processing:
    """ mainly, consisting of 
        * module preprocess - for remove special chars, lower case, etc
        * module tokenizer  - for tokenization task
    """
    def __init__(self, verbose:bool=False):
        self._preprocess = None
        self._tokenizer  = None
        #self._tfidf     = None
        self._vocabs    = []
        self._stopwords = []
        self._whitelist = []
        self._blacklist = []
        #self._tf_params = {}
        self._verbose   = verbose

        self.load()
        
    def load(self, **kwargs):
        self.set_vocabs()
        self.set_preprocess()
        #self.set_tokenizer()
        ## self.__set_tfidf_params()
        #self.set_tfidf()
        
    def set_preprocess(self, preprocess=None):
        if preprocess: self._preprocess = preprocess
        else:          self._preprocess = base_processing.preprocess
        
    def set_tokenizer(self, tokenizer=None, vocab=None, keep_whitespace:bool=False):
        """ if tokenizer is not None, set tokenizer by ignoring other params
        """
        if tokenizer: self._tokenizer = tokenizer
        else:
            if vocab: vocab = vocab if type(vocab) is Trie else Trie(vocab)
            self._vocabs    = vocab
            self._tokenizer = base_processing.default_tokenizer(vocab, keep_whitespace)


    def set_vocabs(self, vocabs=None, stopwords=None, whitelist=None, blacklist=None, is_append:bool=True, verbose:bool=None):
        verbose = verbose if verbose is not None else self._verbose
        try:
            # default vocab setting
            if all([vocabs is None, stopwords is None, whitelist is None, blacklist is None]):
                self._vocabs    = Trie( base_processing.thai_words() )
                self._stopwords = Trie( base_processing.thai_stopwords() )
                self._blacklist = []
                self._whitelist = []
                if verbose: print(f'set default vocab set: {len(self._vocabs)} vocabs')
                return
            # process assigned dict
            #vocabs    = vocabs    if vocabs    else []   if vocabs    == [] else None
            #stopwords = stopwords if stopwords else None if stopwords == [] else None
            #whitelist = whitelist if whitelist else None if whitelist == [] else None
            #blacklist = blacklist if blacklist else None if blacklist == [] else None

            new_vocab = []
            if vocabs:    new_vocab += vocabs 
            if stopwords: new_vocab += stopwords 
            if whitelist: new_vocab += whitelist 
            if blacklist: new_vocab += blacklist

            if is_append:
                # adding assigned dict to original
                if new_vocab: self._vocabs    = Trie(list(self._vocabs)    + new_vocab)
                if stopwords: self._stopwords = Trie(list(self._stopwords) + stopwords)
                if whitelist: self._whitelist = Trie(list(self._whitelist) + whitelist)
                if blacklist: self._blacklist = Trie(list(self._blacklist) + blacklist)
                if verbose: print(f'append new vocabs: {len(self._vocabs)} vocabs')
            else:
                # set new assigned dict
                if new_vocab == []: new_vocab = [' ']  # error prevention
                if vocabs    is not None: self._vocabs    = Trie(new_vocab)
                else:                     self._vocabs    = Trie(list(self._vocabs) + new_vocab)
                if stopwords is not None: self._stopwords = Trie(stopwords)
                if whitelist is not None: self._whitelist = Trie(whitelist)
                if blacklist is not None: self._blacklist = Trie(blacklist)
                if verbose: print(f'set new vocabs: {len(self._vocabs)} vocabs')

        except Exception as e:
            raise(e)

        finally:
            self.update_setting()


#    def set_tfidf(self, tfidf:TfidfVectorizer=None, **kwargs):
#        """ if tfidf is set, ignore the kwargs
#        """
#        try:
#            if tfidf: self._tfidf = tfidf
#            else:     
#                if kwargs: self.__set_tfidf_params(**kwargs)
#                self._tfidf = TfidfVectorizer(**self._tf_params)
#        except Exception as e:
#            raise e
            

#    def __set_tfidf_params(self, is_update:bool=True, **kwargs):
#        if kwargs: 
#            if is_update: self._tf_params.update(kwargs)
#            else:         self._tf_params = kwargs
#        else:      self._tf_params = {'ngram_range':(1,2), 'max_df': 0.9, 'min_df': 20, 
#                                      'max_features': 8_000, 
#                                      'preprocessor': self.preprocess, 
#                                      'tokenizer': self._tokenizer,
#                                      'stop_words': list(self._stopwords)
#                                     }

    def update_setting(self):
        """ after update vocab set, should be update tokenizer & tfidf as well
            ISSUES: this setting focus on using default tokenizer 
        """
        self.set_tokenizer(tokenizer=None, vocab=self._vocabs)
#        self.set_tfidf(preprocessor=self.preprocess, tokenizer=self._tokenizer, stop_words=self._stopwords)
            
            
    def tokenize(self, text, do_preprocess:bool=True, mode='token') -> list:
        if do_preprocess: text = self.preprocess(text)
        token_sent = self._tokenizer(text)
        if mode == 'token':
            return token_sent
        else:
            return ' '.join([re.sub(' ', '_', token) for token in token_sent])
            # return ' '.join(['_'.join(token.split()) for token in token_sent])
  





class keyterm_extractor:
    """ do keyterm extraction from list of token_text by fit( token_texts ) and extract()
        if the input is list of plaintext, fit( texts ) and extract() is used
    """
    PACKAGE = {
                'S': {'ngram_range': (1,3),
                      'min_df': 1,
                      'max_features': 5_000,
                     },
                'L': {'ngram_range': (1,5),
                      'max_df': 0.9,
                      'min_df': 20,
                      'max_features': 8_000,
                     }
              }


    def __init__(self, tp:text_processing=None, count_vec:CountVectorizer=None, verbose:bool=False, **kwargs):
        self.load(tp=tp, count_vec=count_vec, verbose=verbose, **kwargs)


    def reset(self):
        # package
        self._package   = 'C' # custom
        # tokenizer
        self._tokenize  = None
        # tokenizer module including preprocessing and postprocessing
        self._tp        = None
        # CountVectorizer
        self._countv    = None
        # Tfidf
        self._tfidf     = None
        # dataframe of features for keyterm extraction
        self._matrix    = None
        # dataframe of content e.g., text, tokened text
        self._content   = None
        # verbose
        self._verbose   = False


    #@classmethod
    def _validate_count_vectorizer(self, count_vec:CountVectorizer=None, **kwargs):
        """ if count_vec is set, return
            else crafting parameters of count_vec base on given {kwargs}
        """
        # if count_vec is set, return count_vec
        if count_vec:
            tokenizer = count_vec.get_params().get('tokenizer')
            if tokenizer is None:
                count_vec.set_params(tokenizer=self._tp.tokenize)
            return count_vec

        # get default params of CountVectorizer
        params         = CountVectorizer().get_params()
        # update related params from package
        package        = kwargs.get('package', 'S') 
        package        = self._validate_package(package)
        related_params = keyterm_extractor.PACKAGE[package]
        params.update(related_params)
        # update tokenizer if tp is set
        if self._tp:    params.update({'tokenizer': self._tp.tokenize})
        # update related params from kwargs (kwargs overwrite other params)
        related_params = {k: v for k, v in kwargs.items() if k in params}
        params.update(related_params)

        # finalize CountVectorizer
        cv = CountVectorizer(**params)
        return cv


    @classmethod
    def _validate_tokenizer(cls, count_vec:CountVectorizer):
        """ extract tokenizer of the given {count_vec}
        """
        params = count_vec.get_params()
        return params['tokenizer']


    @classmethod
    def _validate_text_processing(cls, tp:text_processing=None):
        """ return default text_processing if None
            tp is used when fit() with plain text
        """
        # HANDLE TP TOKENIZER (tp)
        if tp is None: tp = text_processing()
        return tp


    #@classmethod
    def _validate_package(self, package:str='S'):
        """ validate if the given package is in the PACKAGE or not
            'S' returned if package is invalid
        """
        if package in self.PACKAGE:
            self._package = package
            return package
        else:
            raise ValueError(f'package "{package}" not found, try to use {", ".join(self.PACKAGE)}')

    # --------------------------------
    # keyterm_extractor: construction
    # --------------------------------
    @classmethod
    def from_package(cls, package:str='S', tp:text_processing=None, verbose:bool=False, **kwargs):
        kwargs.update({'package': package})
        return cls(tp=tp, **kwargs, verbose=verbose)


    def load(self, count_vec:CountVectorizer=None, tp:text_processing=None, verbose:bool=False, **kwargs):
        """ count_vec - how to validate candidate token (ngram, min_df, max_df) including how tokenizing terms
            tp        - in case the input is {text} not {token_text} tokenization with preprocessing needed (not the objective of the class)
            kwargs    - in case of generating count_vec by parameters
        """
        self.reset()
        self._verbose   = verbose
        # be used when fit() with text (not token_text)
        self._tp        = self._validate_text_processing(tp)
        # generate countv without caring of tokenizer
        self._countv    = self._validate_count_vectorizer(count_vec, **kwargs)
        # extract default tokenizer from count_vec, if it is none then use tp.tokenizer instead
        self._tokenize  = self._validate_tokenizer(self._countv)


    # -----------------------
    # keyterm_extractor: fit
    # -----------------------
    def _adaptive_countvectorizer(self, mode:str):
        """ select proper tokenizer regarding the fit() mode -- [text, token_text]
            fit() with token_texts, the tokenizer should be split()
            fit() with texts, the tokenizer should be custom tokenizer
        """
        params = self._countv.get_params()
        if   mode == 'text':
            tokenizer = self._tokenize if self._tokenize is not None else self._tp.tokenize
        else: # mode = token_text
            tokenizer = lambda t: t.split()

        self._countv.set_params(tokenizer=tokenizer)


    def _validate_content(self, content, do_tokenize:bool=True, verbose:bool=None):
        """ - if texts is set, then tokenizing texts to token_texts
            - fetch token_texts to dataframe
            - return related tokenizer
        """
        verbose = self._verbose if verbose is None else verbose
        if verbose: print(f' > processing content..', end='')

        df = pd.DataFrame({'text': content})
        if do_tokenize:
            df['token_text'] = df['text'].apply(lambda v: ' '.join(self._tokenize(v)))
        else:
            df['token_text'] = df['text']
        df['n_token'       ] = df['token_text'].apply(lambda v: len(v.split()))
        self._content = df
        if verbose: print(f'done')


    def _validate_mask(self, mask=None):
        if mask is None: mask = self._content.shape[0] * [True]
        return mask


    def _sync_tfidf_countvec(self):
        """ copy related params of assigned count_vec to newly created tfidf
        """
        # get initial params
        tfidf_params  = TfidfVectorizer().get_params()
        # sync params
        tx_params = {k: v for k, v in self._countv.get_params().items() if k in tfidf_params}
        tfidf_params.update(tx_params)
        # create tfidf
        self._tfidf = TfidfVectorizer(**tx_params)


    def _fit_content(self, mask=None, verbose:bool=None):
        """ fit content with tfidf and counter_vec
            * if the package does not proper, make it right
            * sync params of both tfidf and count_vec
        """
        verbose = self._verbose if verbose is None else verbose
        if verbose: print(f' > fit content..', end='')
        # validate mask
        mask = self._validate_mask(mask)
        # fit on count_vec .. if error then change to S package
        try:
            self._countv.fit(self._content.loc[mask, 'token_text'])
        except:
            if verbose: print(f'\n   > adaptive for small corpus..', end='')
            self._countv = self._validate_count_vectorizer()
            self._countv.fit(self._content.loc[mask, 'token_text'])
        # create tfidf
        self._sync_tfidf_countvec()
        # fit on tfidf
        self._tfidf.fit(self._content.loc[mask, 'token_text'])
        if verbose: print(f'done')


    def _create_candidate_matrix(self, mask=None, verbose:bool=None):
        verbose = self._verbose if verbose is None else verbose
        if verbose: print(f' > create candidate matrix..', end='')
        # validate mask
        mask    = self._validate_mask(mask)
        # create candidate matrix
        tfdf    = pd.DataFrame(self._tfidf.idf_, index=self._tfidf.get_feature_names_out(), columns=['idf'])
        ct_feat = self._countv.transform(self._content.loc[mask, 'token_text'])
        ctdf    = pd.DataFrame(ct_feat.toarray().sum(axis=0), index=self._countv.get_feature_names_out(), columns=['count'])
        self._matrix = pd.DataFrame({'idf': self._tfidf.idf_, 'count': ct_feat.toarray().sum(axis=0)}, index=self._tfidf.get_feature_names_out())
        del ct_feat
        if verbose: print('done')


    def _calc_features(self, mask, verbose:bool=None):
        verbose = self._verbose if verbose is None else verbose
        if verbose: print(f' > extract features..', end='')
        _tb         = lambda key: self._matrix.loc[self._matrix.index==key, 'count'].values
        _freq       = lambda val: val[0] if len(val) else 1
        _each_count = lambda tokens: [_freq(_tb(tk)) for tk in self._tp.tokenize(tokens)]

        self._matrix['each_count']  = [_each_count(t) for t in self._matrix.index.to_list()]
        self._matrix['min_count']   = self._matrix.each_count.apply(min)
        self._matrix['min_ratio']   = self._matrix.apply(lambda r: r['count']/r['min_count'], axis=1)
        self._matrix['ngram']       = self._matrix.each_count.apply(len)

        self._matrix['start_ratio'] = self._matrix.apply(lambda r: r['count']/r['each_count'][ 0], axis=1)
        self._matrix['last_ratio']  = self._matrix.apply(lambda r: r['count']/r['each_count'][-1], axis=1)
        self._matrix['average']     = self._matrix.apply(lambda r: (r['min_ratio'] + r['start_ratio'] + r['last_ratio'])/3, axis=1)
        if verbose: print(f'done')



    def fit(self, content, do_tokenize:bool=True, n_token:int=0, verbose:bool=None):
        """ fitting content for keyterm extraction
            * content     - could be list of {plain_text, token_text, dataframe}
            * do_tokenize - true if content requiring tokenization, else false for as-is content
            * n_token     - minimum token size that will be considered
            * verbose     - printing message if it is set, otherwise use class.verbose
        """
        try:
            verbose = self._verbose if verbose is None else verbose
            # convert content into token_text format
            self._validate_content(content, do_tokenize, verbose)
            # verify proper condition for keyterm extraion
            mask    = self._content.n_token > n_token
            # make sure countv and tfidf have the same setting
            self._fit_content(mask, verbose)
            # create keyterm candidate matrix
            self._create_candidate_matrix(mask, verbose)
            # extracting features
            self._calc_features(verbose)

        except Exception as e:
            raise e


    # ---------------------------
    # keyterm_extractor: extract 
    # ---------------------------
    def __assigned_tuple(self, val, default):
        try:
            if   type(val) == int:   val = float(val)
            if   type(val) == float: val = (val, val)
            elif type(val) == tuple or type(val) == list: 
                val = val if len(val) == 2 else default
            else:                    val = default
        except: 
            val = default
        finally:
            return val

        
    def __remove_subtext(self, candidate):
        B = BTrie(candidate)
        keyterms = [t for t in B.keys() if len(B.keys(t)) == 1 and len(B.bkeys(t)) == 1]
        return keyterms

    
    def __shrink_terms(self, token_terms, df, threshold:float=0.7):
        # reformat
        df = df.loc[df.index.isin(token_terms)]
        df = df.reset_index().rename(columns={'index': 'candidate'})
        # shrink text
        df['shrink'] = df['candidate'].apply(lambda v: ''.join(v.split()))
        # prepare features
        df['c_text'] = df['candidate'].apply(lambda v: self._content['text'].str.contains(v).sum())
        df['s_text'] = df['shrink'   ].apply(lambda v: self._content['text'].str.contains(v).sum())
        # calc mask
        df['c_mask'] = df.apply(lambda r: r['c_text']/r['count'] > threshold,  axis=1)
        df['s_mask'] = df.apply(lambda r: r['s_text']/r['count'] > threshold,  axis=1)
        df['revise'] = df.apply(lambda r: not any([r['c_mask'], r['s_mask']]), axis=1)
        # sorting
        df.sort_values(by=['ngram', 'average'], ascending=False)


        df = df[['candidate', 'shrink', 'ngram', 'count', 'c_text', 's_text', 'c_mask', 's_mask', 'revise']]

        return df

            
    def extract(self, top_n:int=30, package:str='S', idf:float=None, average:float=None, threshold=None, ratio=None, mode='text', verbose:bool=None):
        verbose = self._verbose if verbose is None else verbose
        package = package.upper() if package               else 'S'
        package = package         if package in ['S', 'L'] else 'S'
        if package == 'S':
            threshold = self.__assigned_tuple(threshold, (0.4, 0.4))
            ratio     = self.__assigned_tuple(ratio, (0.0, 1.1))
            idf       = idf if idf else 0.
            average   = average if average else 0.5
        else:
            threshold = self.__assigned_tuple(threshold, (0.0, 0.0))
            ratio     = self.__assigned_tuple(ratio, (0.1, 1.1))
            idf       = idf if idf else 6.0
            average   = average if average else 0.3
        mode      = mode if mode in ['debug', 'text', 'token', 'table'] else 'text'
        
        if verbose: print(f'PACKAGE: {package}\nthreshold: {threshold}\nratio: {ratio}\nidf: {idf}\naverage: {average}')

        try:
            candidate = self._matrix.loc[(self._matrix['ngram']  > 1) & 
                                    (self._matrix['count']       > 1) &
                                    (self._matrix['start_ratio'] > threshold[0]) & 
                                    (self._matrix['last_ratio']  > threshold[1]) &
                                    (self._matrix['min_ratio']   > ratio[0])     &
                                    (self._matrix['min_ratio']   < ratio[1])     &
                                    (self._matrix['idf']         > idf)          &
                                    (self._matrix['average']   > average) 
                                   ].sort_values(by=['ngram', 'average'], ascending=False)[:top_n]
            if verbose: print(f' > {candidate.shape[0]} candidates from original {self._matrix.shape[0]} candidates')
            if mode == 'debug': return candidate

            # grouping with trie here
            token_terms = candidate.index.to_list()
            token_terms = self.__remove_subtext(token_terms)
            if verbose: print(f' > {len(token_terms)} candidates after remove subtext')
            if mode == 'token': return token_terms

            # extract table of keyterms
            candidate = self.__shrink_terms(token_terms, candidate)

            # display result
            keyterms  = candidate[candidate['c_mask']]['candidate'].to_list() + candidate[candidate['s_mask']]['shrink'].to_list()
            revise    = candidate[candidate['revise']]['candidate'].to_list()
            total_keyterms = keyterms + revise
            if verbose: print(f' > {len(total_keyterms)} keyterms extracted, {len(keyterms)} and {len(revise)} high and low confidence, respectively')
            if mode == 'table': return candidate

            return total_keyterms

        except Exception as e:
            print(f' > exception {str(e)}')
            if mode=='table': return None
            if mode=='text' : return []
            raise e

    
    def NOTE(self):
        """ [o] CONCERN
            tokenizer with vocab = '' (empty string)
        """
        """ should the user know what to do?
            maybe ignore the count_vectorizer part 
            just load() or load(tokenizer) and 
            just fit() and fit_tokenized_corpus()
            params - tokenizer_type
                   - 
        """
        """ case finalized
            * defaoult: (cv) -> any cv - could enhance by tp / stopword
            * from_configure ( cv=ngram, min_df, max_df)
            * from_package(package)
            * load_advance(cv, tp, stopword)
            * fit_tokened_text(token_text)
            * fit(text, tp=None, stopwords=None, n_token)


        """
        """ cases of construction
            * default: (tp, cv)
            * from configure( tp=vocab, cv=ngram, min_df, max_df)
            * from package(   tp=vocab, cv=package)

            * fit(content)
            * - text_token using tokenizer = split
            * - text       using tokenizer = tp
        """
        ...
