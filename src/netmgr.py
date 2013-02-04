#!/usr/bin/python
# -*- coding: utf-8 -*-


from db_modules import Rack,DeviceClass,DeviceNode,DeviceType,DeviceRackPos,NetworkPort
from db_modules import ManageIP,PublicIP,VLANInfo
from flask import Blueprint,render_template

netmgr_page = Blueprint('netmgr_page', __name__)
__author__ = 'ChenLong'



@netmgr_page.route('/')
def netmgr_index():
    return render_template('netmgr/netmgr.html')