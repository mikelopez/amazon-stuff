from lettuce import step, before, world
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals, assert_true

import sys
sys.path.append('lib/amazon')
from AmazonAPI import Amazon

@step(u'Given I instantiate "(.*)"')
def given_i_instantiate_group1(step, classname):
  world.set_class = None
  world.set_class = eval(classname)
  assert_true(world.set_class)

@step(u'Class should contain "(.*)" method')
def class_should_contain_group1_method(step, methodname):
  assert_true(hasattr(world.set_class, methodname))

@step(u'Variable "(.*)" should be None')
def variable_group1_should_be_none(step, var):
  assert_true(getattr(world.set_class, var) is None)

@step(u'Class should contain "(.*)" dict with "(.*)" key')
def class_should_contain_group1_dict_with_group2_key(step, var, key):
  assert_true(key in getattr(world.set_class, var).keys())

