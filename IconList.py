#!/usr/bin/python
# coding: utf-8
#
#from fitting_models import Mobile
import urllib
from urllib2 import HTTPError
from string import Template


class Mobile_icon_list():
	"""
	docstring for Mobile_icon_list.
	"""

	def __init__(self):
		"""
		インスタンスを生成した時に、
		fitting.model　から　レコード　を取得
		"""
#テスト用の仮データ
		self.records = {"num":3825, "gid":'TY0000050', "yid":'201204-999999', "jfpdf":'2',"fitting":'null', "recomm":'', "pulse":'',"disasm":'0'} #Mobile.objectsが使えないため一時的に作成、init実装後にコメントアウトする
#		self.records = Mobile.objects.order_by('num').all()

	def get_url(self, record):
		"""
		>>> r2 = {"num":3825, "gid":'TY0000050', "yid":'201204-999999', "jfpdf":'null',"fitting":'null', "recomm":'null', "pulse":'null',"disasm":'null'}
		>>> tmp_list = Mobile_icon_list()
		>>> tmp_list.get_url(r2)
		'/TY0000050_201204-999999/'
		"""
		url = Template('/${gid}_$yid/')
		return url.substitute(gid = record["gid"], yid = record["yid"])

	def set_null(self, key, url):
		"""
		>>> tmp_list = Mobile_icon_list()
		>>> url = '/jfpdf/TY0000050_201204-999999/'
		>>> key = 'jfpdf'
		>>> tmp_list = Mobile_icon_list()
		>>> tmp_list.set_null(key, url)
		>>> tmp_list.records[key]
		''
		"""
		try:
			test = Mobile_link_test()
			test.mobile_link_test(url)
		except NameError:
			self.records[key] = ''

	def trim_record(self):
		"""
		すべてnullならレコードごと削除
		削除前のレコード数　＝　削除したレコード　+ 削除後のレコード数

		pk　の num で指定する場合
		trim_num = r["num"]
		Mobile.objects.filter(num=trim_num).delete()


		クエリで指定する場合
		Mobile.objects.filter(jfpdf='null')
		.filter(fitting='null')
		.filter(recomm='null')
		.filter(pulse='null')
		.filter(disasm='null')
		.delete()
		"""
		pass

class Mobile_link_test():

	def mobile_link_test(self, url):
		"""
		一時的にすべてNameErrorを出すようにしておく
		あとで　NameError　→　HTTPError　に置き換える

		>>> url = '/jspdf/TY0000050_201204-999999'
		>>> test = Mobile_link_test()
		>>> test.mobile_link_test(url)
		Traceback (most recent call last):
		NameError
		"""
		raise NameError


if __name__ == '__main__':
	"""
	jfpdf、fitting、recomm、pulse、disasm　の5種類のkeyごとに,
	valueに値が入っていれば,set_nullメソッドを呼び出す
	for で展開すると　dict が　str　になってしまう
	多分、本番データを遣って、もう一階層上で　for　展開すれば大丈夫なはず
	"""
	tmp_list = Mobile_icon_list()
	for key in tmp_list.records:
		url = tmp_list.get_url(tmp_list.records)
		if key == 'jfpdf' and tmp_list.records['jfpdf'] != '':
			url = '/jfpdf' + url
			tmp_list.set_null('jfpdf', url)
		elif key == 'fitting' and tmp_list.records['fitting'] != '':
			url = '/fitting' + url
			tmp_list.set_null('fitting', url)
		elif key == 'recomm' and tmp_list.records['recomm'] != '':
			url = '/recomm' + url
			tmp_list.set_null('fitting', url)
		elif key == 'pulse' and tmp_list.records['pulse'] != '':
			url = '/pulse' + url
			tmp_list.set_null('pulse', url)
		elif key == 'disasm' and tmp_list.records['disasm'] != '':
			url = '/disasm' + url
			tmp_list.set_null('disasm', url)
#			save()
#			tmp_list.trim_record()

import doctest
doctest.testmod()
