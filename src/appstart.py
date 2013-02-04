#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask,url_for,render_template,redirect
from flask.ext.sqlalchemy import SQLAlchemy

from appenv import app,db
from instdev import instdev_page
from devmgr import  devmgr_page
from netmgr import netmgr_page
from report import report_page

from db_modules import Rack,DeviceClass,DeviceNode,DeviceType,DeviceRackPos,NetworkPort
from db_modules import ManageIP,PublicIP,VLANInfo



@app.route('/')
def redirect_instdev():
    return redirect('/instdev')
#    return render_template('frontpage.html')

app.register_blueprint(instdev_page, url_prefix='/instdev')
app.register_blueprint(devmgr_page, url_prefix='/devmgr')
app.register_blueprint(netmgr_page, url_prefix='/netmgr')
app.register_blueprint(report_page, url_prefix='/report')


if __name__ == '__main__':
    app.run()
