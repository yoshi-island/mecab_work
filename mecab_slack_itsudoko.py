#!/usr/bin/env python
# -*- coding:utf-8 -*-

# slackのチャンネルの内容をサマる

import sys
import MeCab
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error
import json
import random



# 指定する変数
# token
import password_list
token = password_list.token

## 対象チャンネル名は引数として指定できる(デフォルトは#random)
channel_name = sys.argv
if len(channel_name) == 1:
  channel_name.append("random")
channel_name = channel_name[1]



# 受け取った文章をMecabで解析する
def mecab_perse(text=None):
  m = MeCab.Tagger ("-Ochasen")
  if text != None:
    #print(m.parse (text))
    return m.parse (text)
  else:
    #print(m.parse ("すもももももももものうち"))
    return m.parse ("すもももももももものうち")



# Slackで受け取ったチャンネル名からチャンネルIDを返す
def get_slack_channel_id(token=None, channel_name=None):
  url = "https://slack.com/api/channels.list"
  if token == None:
    return "error"

  params = {
    "token": token,
    "exclude_archived": "true"
    }

  req = urllib.request.Request(url)
  req.add_header('Content-Type', 'application/x-www-form-urlencoded')
  params = urllib.parse.urlencode(params).encode('utf-8')
  channel_data = urllib.request.urlopen(req, params).read().decode("utf-8")

  channel_json_dict = json.loads(channel_data)
  channel_json_dict = channel_json_dict["channels"]

  for line in channel_json_dict:
    if line["name"] == channel_name:
      #print(line["id"])
      return line["id"]
  return "error"



# SlackのチャンネルIDから会話の内容を一行ずつリスト形式で取得する
def get_slack_chat(token=None, channel_id=None, count=100):
  url = "https://slack.com/api/channels.history"
  if token == None:
    return "error"

  params = {
    "token": token,
    "channel": channel_id,
    "count": count,
    }

  req = urllib.request.Request(url)
  req.add_header('Content-Type', 'application/x-www-form-urlencoded')
  params = urllib.parse.urlencode(params).encode('utf-8')
  chat_data = urllib.request.urlopen(req, params).read().decode("utf-8")

  chat_data_json_dict = json.loads(chat_data)
  chat_data_json_dict = chat_data_json_dict["messages"]
  #print(chat_data_json_dict)

  chat_data_list = []
  for line in chat_data_json_dict:
    chat_data_list.append(line["text"])
  #print(chat_data_list)
  return chat_data_list



# 会話のリストからランダムに指定した品詞を取り出す
def get_hinshi(text=None, hinshi=None, nglist=[]):
  ## 受け取ったテキストをmecab_perse関数を使って解析
  persed_text = mecab_perse(text)

  ## 解析した結果をリスト形式にする
  text_list_temp = persed_text.split("\n")
  text_list = []
  for l in text_list_temp:
    text_list.append(l.split("\t"))

  ## 指定した品詞を取り出す
  results_list = []
  for l in text_list:
    if len(l) > 1: #EOSとか空行を省く
      if l[3] == hinshi:
        check_flag = 0
        for nl in nglist: #nglistのワードを省く
          if str(l[2]) == str(nl):
            check_flag += 1
        if check_flag == 0:
          results_list.append(l[2])
  #print(results_list)
  return results_list



# 実行
if __name__ == "__main__":
  ## チャット会話を取得
  channel_id = get_slack_channel_id(token, channel_name)
  chat_list = get_slack_chat(token, channel_id, 100)

  ## 動詞をリストで取得
  verb_list = []
  for cl in chat_list:
    verb_line = get_hinshi(cl, "動詞-自立", ["する", "なさる", "なる", "ある"])
    verb_list = verb_list + verb_line
  #print(verb_list)

  ## 名詞をリストで取得
  noun_list = []
  for cl in chat_list:
    noun_line = get_hinshi(cl, "名詞-一般")
    noun_list = noun_list + noun_line
  #print(noun_list)

  ## 地域をリストで取得
  place_list = []
  for cl in chat_list:
    place_line = get_hinshi(cl, "名詞-固有名詞-地域-一般")
    place_list = place_list + place_line
  #print(place_list)

  ## 文字列成形
  if len(verb_list) > 0:
    doushita = random.choice(verb_list) + "。"
  else:
    doushita = ""
  if len(place_list) > 0:
    dokode  = random.choice(place_list) + "で"
  else:
    dokode = ""
  if len(noun_list) > 0:
    naniga = random.choice(noun_list) + "が"
  else:
    naniga = ""
  if len(noun_list) > 0:
    naniwo = random.choice(noun_list) + "を"
  else:
    naniwo = ""
  itsudoko_line = dokode + naniga + naniwo + doushita
  print("%s、、、「#%s」はそんなチャンネルです。" % (itsudoko_line, channel_name))
