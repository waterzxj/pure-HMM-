#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import os
import sys
import math


curret_path = os.path.abspath(__file__)
curret_dir = os.path.dirname(curret_path)

#wordseg_path = curret_dir + "../wordseg"
#print wordseg_path
sys.path.append(sys.path[0] + "/../")

#from wordseg.load_hmm import load_segment_corpus
from load_hmm import STATS, load_hmm, UNK
from utils import strdecode
from collections import defaultdict

def viterbi(sentence, start_vec_prob, trans_vec_prob, emission_vec_prob):
    """
    do viterbi decode
    """
    sentence = strdecode(sentence)
    if len(sentence) == 0:
        return

    cal_dict = defaultdict(lambda:defaultdict(float))
    stat_dict = defaultdict(list)
    #start
    for stat in STATS:
        obs = sentence[0] if sentence[0] in emission_vec_prob[stat] else UNK
        cal_dict[0][stat] =  math.log(emission_vec_prob[stat][obs]) + math.log(start_vec_prob[stat]) 
        stat_dict[stat] = [stat]
        
    for num in range(1, len(sentence)):
        new_stat_dict = defaultdict(list)
        for stat in STATS:
            obs = sentence[num] if sentence[num] in emission_vec_prob[stat] else UNK    
            prob, _stat = max([((cal_dict[num - 1][_stat] + math.log(trans_vec_prob[_stat][stat]) + math.log(emission_vec_prob[stat][obs])), _stat) for _stat in STATS])
                    
            cal_dict[num][stat] = prob
            new_stat_dict[stat] = stat_dict[_stat] + list(stat)
        stat_dict = new_stat_dict    

    #根据最后一个状态进行译码
    prob, stat = max([(cal_dict[len(sentence) - 1][_stat],_stat) for _stat in STATS])
    print "stat", stat
    path = stat_dict[stat]
    return prob,path


if __name__ == "__main__":
    from load_hmm import load_hmm
    corpus_file = "../wordseg/icwb2-data/training/pku_training.utf8"
    start_vec_probs, trans_vec_probs, emission_vec_probs = load_hmm(corpus_file)
#    start_vec_probs, trans_vec_probs, emission_vec_probs = load_segment_corpus(corpus_file, '  ')
    query = '今天是个晴天'
    prob, path = viterbi(query,start_vec_probs, trans_vec_probs, emission_vec_probs)
    print prob
    print "->".join(path)

