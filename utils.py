#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import os,sys

def strdecode(sentence):
    """
    decode sentence to unicode
    """
    if not isinstance(sentence, unicode):
        try:
            sentence = sentence.decode("utf-8")
        except:
            sentence = sentence.decode("gbk")
    return sentence    

if __name__ == "__main__":
    t_s = "我是一名人"
    print type(t_s)
    print type(strdecode(t_s))
