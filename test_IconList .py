#!/usr/bin/python
# coding: utf-8

from IconList import *
import unittest
import urllib
from urllib2 import HTTPError
from string import Template

#テストデータ
r1 = {"num":3825, "gid":'TY0000050', "yid":'201204-999999', "jfpdf":2,
"fitting":'', "recomm":'', "pulse":'', "disasm":''}
r2 = {"num":3825, "gid":'TY0000050', "yid":'201204-999999', "jfpdf":'null',
"fitting":'null', "recomm":'null', "pulse":'null',
"disasm":'null'}


tmp_list = Mobile_icon_list()
url = '/jfpdf//TY0000050_201204-999999/'
key = 'jspdf'

class Test(unittest.TestCase):
#	def test_set_null(self):
#		self.assertEquals(set_null(r, key), )


	def test_set_null(self):
		self.assertEquals(tmp_list.set_null(key, url), 'foo')






if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_list']
    unittest.main()
