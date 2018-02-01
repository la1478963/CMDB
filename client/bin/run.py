#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from client.core.func import GetHostInfo


JG_info=GetHostInfo()
# JG_func=JG_info._begin()


