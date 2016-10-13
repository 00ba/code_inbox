#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
AccessからPostgreSQLにエクスポートされたmobileテーブルには、
すでに削除されたFittingやRecommendのデータが、"データ有"のマークのまま残っている。
この修復作業を行い、PostgreSQL上のデータを正しい状態にする。
"""


import os, sys
from string import Template

from django.conf import settings
sys.path.append(os.pardir)  # pardir = 親ディレクトリ
os.environ['DJANGO_SETTINGS_MODULE']="crz.settings"
# こうしておくと、LANG=ja_JP.eucJPなKtermでもエラーを起こさず出力できる
os.environ['LANG']="ja_JP.UTF-8"
from django.test import TestCase
from django.test.client import Client
from django.http import Http404

from fitting.models import Mobile

class Mobile_icon_list():

   def __init__(self):
       """
       インスタンスを生成した際に、fitting.modelから全レコードを取得する
       """
   records = Mobile.objects.order_by('num').all()


   def get_url(self, matched_key, record):
       """
       レコードのデータからリンクテスト用のurlを生成する
	   record = {'yid': u'201112-201411', 'num': 149190, 'recomm':None, 'mkid': 7, 'car': u'\u30a4\u30f3\u30d7\u30ec\u30c3\u30b5G4\uff08H23/12\u301cH26/11\uff09', 'after': 12010, 'pulse': 2, 'disasm': 2,'subid': u'G4', 'fitting': 2, 'gid': u'SB0000400', 'jfpdf': 2}
		tmp_list = Mobile_icon_list()
		tmp_list.get_url('jfpdf', record)
       u'/jfpdf/SB0000400%5EG4_201112-201411/'
       """
       if record['subid'] is None:
           url = Template('/$key/${gid}_$yid/')
           return url.substitute(key= matched_key, gid = record['gid'], yid = record['yid'])
       else:
           url = Template('/$key/${gid}%5E${subid}_$yid/')
           return url.substitute(key= matched_key, gid = record['gid'],subid= record['subid'] ,yid = record['yid'])

   def trim_record(self):
       """
       jfpdf,fitting,recomm,pulse,disasm 5フィールドすべてNoneならレコードごと削除
       """

       print "処理前レコード数"
       print self.records.count()
       print "削除レコード数"
       print self.records.filter(jfpdf=None).filter(fitting=None).filter(recomm=None).filter(pulse=None).filter(disasm=None).count()
	   self.records.filter(jfpdf=None).filter(fitting=None).filter(recomm=None).filter(pulse=None).filter(disasm=None).delete()
       print "処理後レコード数"
       print self.records.count()


class Mobile_link_test(TestCase):

   def mobile_link_test(self, url):
       """
       各フィールドから生成されたurlが存在するかチェック

       存在しないurlでテスト
	   url = '/jspdf/TY0000000_201204-999999/'
	   test = Mobile_link_test('mobile_link_test')
	   test.mobile_link_test(url)
       404
       """
       # ログイン
       client = Client()
       # ************** user/password ***************
       client.login(username="tester", password="5aGtEagk")
       response = client.get(url)
       return response.status_code


if __name__ == '__main__':
   """
   records:Modelsの全レコード QuerySetオブジェクト
   record:個別のレコード　dicオブジェクト
   key:レコードのフィールド名 strオブジェクト

   keyがjfpdf,fitting,recomm,pulse,disasmのどれかと一致し、
   かつvalueに値が存在すれば,link_testを呼び出す
  404エラーが出たフィールドには、Noneを代入
   その後、全レコードに対してtrim-recordを適用
   """

   test = Mobile_link_test('mobile_link_test')
   tmp_list = Mobile_icon_list()
   for record in tmp_list.records.values():
   #        print record
       for key in record:
   #            None の判定がうまくいかないのでコメントアウト
   #            target_keys = ['jfpdf', 'fitting', 'recomm', 'pulse','disasm']
   #            [tmp_list.set_None(matched_key, record)
   #            for matched_key in target_keys
   #            if key in target_keys and record[key] is not None]
           try:
               if key == 'jfpdf' and record['jfpdf'] is not None:
                   url = tmp_list.get_url('jfpdf', record)
                   test.mobile_link_test(url)
               elif key == 'fitting' and record['fitting'] is not None:
                   url = tmp_list.get_url('fitting', record)
                   test.mobile_link_test(url)
               elif key == 'recomm' and record['recomm'] is not None:
                   url = tmp_list.get_url('recomm', record)
                   test.mobile_link_test(url)
               elif key == 'pulse' and record['pulse'] is not None:
                   url = tmp_list.get_url('pulse', record)
                   test.mobile_link_test(url)
               elif key == 'disasm' and record['disasm'] is not None:
                   url = tmp_list.get_url('disasm', record)
                   test.mobile_link_test(url)
           except 404:
               if key == 'jfpdf':
				   self.records.filter(num=record['num']).update(jfpdf=None)
               elif key == 'fitting':
				   self.records.filter(num=record['num']).update(fitting=None)
               elif key == 'recomm':
				   self.records.filter(num=record['num']).update(recomm=None)
               elif key == 'pulse':
				   self.records.filter(num=record['num']).update(pulse=None)
               elif key == 'disasm':
				   self.records.filter(num=record['num']).update(disasm=None)
#     except:
#         sys.stderr.write("ERROR : Unexpected error.\n")

   tmp_list.trim_record()
   #    finally:
   #   tmp_list.records.save()


import doctest
doctest.testmod()
