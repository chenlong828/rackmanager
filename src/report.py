#!/usr/bin/python
# -*- coding: utf-8 -*-


from db_modules import Rack,DeviceClass,DeviceNode,DeviceType,DeviceRackPos,NetworkPort
from db_modules import ManageIP,PublicIP,VLANInfo
from flask import Blueprint,render_template

report_page = Blueprint('report_page', __name__)
__author__ = 'ChenLong'



@report_page.route('/')
def report_index():
    return render_template('report/report.html')