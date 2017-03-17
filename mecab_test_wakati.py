#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 分かち書き

import sys
import MeCab

def mecab_perse(args=None):
  m = MeCab.Tagger ("-Owakati")
  if args != None:
    print(m.parse (args))
  else:
    print(m.parse ("すもももももももものうち"))

if __name__ == "__main__":
  args = sys.argv
  if len(args) == 1:
    args.append(None)

  mecab_perse(args[1])
