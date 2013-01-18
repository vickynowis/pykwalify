# -*- coding: utf-8 -*-

""" Unit test for pyKwalify - Core """

# python std library
import re
import os
import sys
import unittest
import logging

# Testhelper class
#from .testhelper import * # TODO: this do not work Oo :: TypeError: attribute name must be string, not 'type'
from tests.testhelper import run as run
from tests.testhelper import TestHelper, Log, logging_regex, gettestcwd, makeTestFolder, removeTestFolder, makeTestFile, removeTestfile, _set_log_lv

# pyKwalify imports
import pykwalify
from pykwalify.core import Core

class TestCore(TestHelper):

    def testCore(self):
        # Test sequence with only string values
        a = ["foo", "bar", "baz"]
        b = {"type": "seq", "sequence": [ {"type": "str"} ] }
        c = Core(source_data = a, schema_data = b)
        c.run_core()

        # Test sequence with defined string content type but data only has integers
        a = [1, 2, 3]
        b = {"type": "seq", "sequence": [ {"type": "str"} ] }
        c = Core(source_data = a, schema_data = b)
        with self.assertRaises(Exception):
            c.run_core()

        a = [1, 2, 3, True, False]
        b = {"type": "seq", "sequence": [ {"type": "int"} ] }
        c = Core(source_data = a, schema_data = b)
        c.run_core()

        a = [True, False]
        b = {"type": "seq", "sequence": [ {"type": "bool"} ] }
        c = Core(source_data = a, schema_data = b)
        c.run_core()

        a = [True, False]
        b = {"type": "seq", "sequence": [ {"type": "str"} ] }
        c = Core(source_data = a, schema_data = b)
        with self.assertRaises(Exception):
            c.run_core()

        a = [True, False, 1]
        b = {"type": "seq", "sequence": [ {"type": "bool"} ] }
        c = Core(source_data = a, schema_data = b)
        with self.assertRaises(Exception):
            c.run_core()

        a = ["foo", "bar", "foobar"]
        b = {"type": "seq", "sequence": [ {"type": "str", "length": {"max": 5, "min": 1} } ] }
        c = Core(source_data = a, schema_data = b)
        with self.assertRaises(Exception):
            c.run_core()

        a = {"name": "foo", "email": "foo@mail.com", "age": 20, "birth": "1985-01-01"}
        b = {"type": "map", "mapping": {"name": {"type": "str", "required": True}, "email": {"type": "str", "pattern": ".+@.+"}, "age": {"type": "int"}, "birth": {"type": "str"} } }
        c = Core(source_data = a, schema_data = b)
        c.run_core()

        a = {"name": "foo", "email": "foo(at)mail.com", "age": "twnty", "birth": "Jun 01, 1985"}
        c = Core(source_data = a, schema_data = b)
        with self.assertRaises(Exception):
            c.run_core()

        a = [ {"name": "foo", "email": "foo@mail.com"}, {"name": "bar", "email": "bar@mail.net"}, {"name": "baz", "email": "baz@mail.org"} ]
        b = {"type": "seq", "sequence": [ {"type": "map", "mapping": {"name": {"type": "str"}, "email": {"type": "str"} } } ] }
        c = Core(source_data = a, schema_data = b)
        c.run_core()

        # TODO: (line 3) [/1] key 'name:' is required. Not working yet
        a = [ {"name": "foo", "email": "foo@mail.com"}, {"naem": "bar", "email": "bar@mail.net"}, {"name": "baz", "mail": "baz@mail.org"} ]
        c = Core(source_data = a, schema_data = b)
        with self.assertRaises(Exception):
            c.run_core()

        a = {"company": "Kuwata lab.", "email": "webmaster@kuwata-lab.com", "employees": [{"code": 101, "name": "foo", "email": "foo@kuwata-lab.com"}, {"code": 102, "name": "bar", "email": "bar@kuwata-lab.com"}] }
        b = {"type": "map", "mapping": {"company": {"type": "str", "required": True}, "email": {"type": "str"}, "employees": {"type": "seq", "sequence": [ {"type": "map", "mapping": {"code": {"type": "int", "required": True}, "name": {"type": "str", "required": True}, "email": {"type": "str"} } } ] } } }
        c = Core(source_data = a, schema_data = b)
        c.run_core()

        # TODO: - (line 9) [/employees/1/mail] key 'mail:' is undefined. Not working yet
        a = {"company": "Kuwata Lab.", "email": "Webmaster@kuwata-lab.com", "employees": [ {"code": "A101", "name": "foo", "email": "foo@kuwta-lab.com"}, {"code": 102, "name": "bar", "email": "bar@kuwata-lab.com"} ] }
        c = Core(source_data = a, schema_data = b)
        with self.assertRaises(Exception):
            c.run_core()

