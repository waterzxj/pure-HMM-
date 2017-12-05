#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import os,sys
from load_hmm import load_hmm
from viterbi import viterbi
from utils import strdecode


def trans_stat_to_token(query, path):
    """
    trans word stat to word token
    """
    query = strdecode(query)
    assert(len(query) == len(path)), "stat length is not equal query length"
    final_res = []
    word = []
    for id in range(len(query)):
        word.append(query[id])
        if path[id] == "S" or path[id] == "E":
            final_res.append(word)
            word = []
    return final_res        


def wordseg(query, hmm_model=None, viterbi_model=None, corpus=None):
    """
    Args:
        query:string
        hmm_mode:func, wordseg model
        corpus:string, hmm corpus
    Return:
        wordseg tokens 
    """
    if hmm_model is None:
        hmm_model = load_hmm

    if viterbi_model is None:
        viterbi_model = viterbi

    if corpus is None:
        corpus = "../wordseg/icwb2-data/training/pku_training.utf8"

    start_prob, trans_prob, emission_prob = hmm_model(corpus)
    prob, path = viterbi_model(query, start_prob, trans_prob, emission_prob)
    print "path  ", path
    final_res = trans_stat_to_token(query, path)
    return final_res

if __name__ == "__main__":
    query = "我毕业于北京邮电大学"
    print "->".join(["".join(item) for item in wordseg(query)])
    


     
