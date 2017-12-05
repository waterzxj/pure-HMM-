# _*_coding:utf-8 _*_
from __future__ import division
import os,sys
import math

from utils import strdecode
from collections import defaultdict

STATS = ("S","B","E","M")
MIN_PROB = 3.14e-100
UNK = "<UNK>"


def transform_word_stat(word_trunk):
    """
    transform the corpus to stats
    """
    stats_list = []
    if len(word_trunk) == 1:
        stats_list.append(STATS[0])
    else:
        stats_list.append(STATS[1])
        for ids in range(1, len(word_trunk) - 1):
            stats_list.append(STATS[3])
        stats_list.append(STATS[2])
    return stats_list
        

def load_hmm(corpus_file, seq="  "):
    """
    load hmm according the according corpus
    """
    start_probs = defaultdict(int)
    trans_probs = defaultdict(lambda : defaultdict(int))
    emission_probs = defaultdict(lambda : defaultdict(int))
    with open(corpus_file) as fin:
        for line in fin:
            #trans line
            stats_list = []
            line = strdecode(line)
            parts = line.rstrip("\n").split(seq)
            line_str = "".join(parts)

            #transform word to stat
            for word in parts:
                stats_list +=  transform_word_stat(word)
            if len(stats_list) <= 0:
                continue
            assert len(line_str) == len(stats_list), "stats length not equal line length"

            #cal the prob
            for idx,stat in enumerate(stats_list):
                if idx == 0:
                    start_probs[stat] += 1
                elif idx >= 1:
                    trans_probs[stats_list[idx - 1]][stats_list[idx]] += 1
                emission_probs[stat][line_str[idx]] += 1

        #trans res prob
        #cal starts vec probs
        start_vec_probs = {}
        start_sum = sum(start_probs.values())
        for k,v in start_probs.iteritems():
            start_vec_probs[k] = v / start_sum
        #tolerance
        for stat in STATS:
            if stat not in start_vec_probs:
                start_vec_probs[stat] = MIN_PROB

        #cal trans vec probs
        trans_vec_probs = defaultdict(lambda : defaultdict(float))
        for k,d in trans_probs.iteritems():
            stat_sum = sum(d.values())
            for _k,v in d.iteritems():
                trans_vec_probs[k][_k] = v / stat_sum
            #tolerance
            for stat in STATS:
                if stat not in trans_vec_probs[k]:
                    trans_vec_probs[k][stat] = MIN_PROB

        #cal emission vec probs
        emission_vec_probs = defaultdict(lambda : defaultdict(float))
        for k,d in emission_probs.iteritems():
            raw_stat_sum = sum(d.values())
            #fine tune 
            len_1 = len([_ for _ in d.values() if _ == 1])
            stat_sum = raw_stat_sum + len_1
            for _k,v in d.iteritems():
                emission_vec_probs[k][_k] = v / stat_sum
            emission_vec_probs[k][UNK] = len_1 / stat_sum
        return start_vec_probs, trans_vec_probs, emission_vec_probs
            
if __name__ == "__main__":
    corpus_file = "../wordseg/icwb2-data/training/pku_training.utf8"
    start_vec_probs, trans_vec_probs, emission_vec_probs = load_hmm(corpus_file)
    print start_vec_probs
    print "E->S", trans_vec_probs["E"]["S"]
    print "E->B", trans_vec_probs["E"]["B"]
    print "emission S 邮", emission_vec_probs["S"][u"邮"]
    print "emission B 邮", emission_vec_probs["B"][u"邮"]
    
