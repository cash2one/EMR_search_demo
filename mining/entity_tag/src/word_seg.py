import sys
import wordseg
sys.path.append('../../')

default_max_term_count = 1024
default_dict_path = '/home/yongsheng/EMR_search_demo/mining/entity_tag/dict/wordseg_dict'

class WordSeg():
    m_dict_loaded = False
    m_dict_handle = None
    m_max_term_count = None
    m_dict_path = None
    m_result_handle = None
    m_token_handle = None
    m_mode = {}
    
    def __init__(self, max_term_count = None, dict_path = None):
        if max_term_count:
            self.m_max_term_count = max_term_count
        else:
            self.m_max_term_count = default_max_term_count
        if not WordSeg.m_dict_loaded:
            if dict_path:
                WordSeg.m_dict_path = dict_path
            else:
                WordSeg.m_dict_path = default_dict_path
            print WordSeg.m_dict_path
            WordSeg.m_dict_handle = wordseg.scw_load_worddict(WordSeg.m_dict_path)
            if WordSeg.m_dict_handle:
                WordSeg.m_dict_loaded = True
        self.m_result_handle = wordseg.scw_create_out(self.m_max_term_count*10)
        self.m_token_handle = wordseg.create_tokens(self.m_max_term_count)
        self.m_token_handle = wordseg.init_tokens(self.m_token_handle, self.m_max_term_count)
        self.m_mode['WPCOMP'] = wordseg.SCW_WPCOMP
        self.m_mode['BASIC'] = wordseg.SCW_BASIC
        self.m_mode['SUBPH'] = wordseg.SCW_SUBPH
        self.m_mode['NEWWORD'] = wordseg.SCW_NEWWORD
        self.m_mode['HUMAN'] = wordseg.SCW_HUMANNAME
        self.m_mode['BOOK'] = wordseg.SCW_BOOKNAME
        self.m_mode['DISAMB'] = wordseg.SCW_DISAMB

    def seg_word(self, word, mode = "BASIC"):
        ret = wordseg.scw_segment_words(WordSeg.m_dict_handle, self.m_result_handle, word, len(word), 1)
        if ret < 0:
            return None
        token_count = wordseg.scw_get_token_1(self.m_result_handle, self.m_mode[mode], self.m_token_handle, self.m_max_term_count)
        l = wordseg.tokens_to_list(self.m_token_handle, token_count)
        ts = []
        for token in l:
            ts.append(token[7])

        return ts
