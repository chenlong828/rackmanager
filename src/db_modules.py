#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'chenlong'

from flask.ext.sqlalchemy import SQLAlchemy

from appenv import app,db

#机房
class Zone(db.Model):
    zone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zone_name = db.Column(db.String(80))
    zone_owner = db.Column(db.String(20))
    zone_phone = db.Column(db.String(20))
    racks = db.relationship('Rack')

#    def __init__(self, zone_name, rack_list=[]): To be continued
#        self.zone_name = zone_name
#        self.racks = rack_list

    def __init__(self, zone_name,zone_owner,zone_phone):
        self.zone_name = zone_name
        self.zone_owner = zone_owner
        self.zone_phone = zone_phone

    def add_rack(self, rack):
        self.racks.append(rack)

#机架
class Rack(db.Model):
    rack_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rack_name = db.Column(db.String(80), unique=True)
    rack_pos = db.Column(db.String(80), unique=True)
    zone_id = db.Column(db.Integer, db.ForeignKey("zone.zone_id"))
    zone = db.relationship('Zone', uselist=False)
    pos_list = db.relation('DeviceRackPos')

    def __init__(self, rack_name, rack_pos, zone_id):
        self.rack_name = rack_name
        self.rack_pos = rack_pos
        self.zone_id = zone_id

#设备供应商
class DeviceVendor(db.Model):
    vendor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_name = db.Column(db.String(80))
    vendor_contact = db.Column(db.String(20))
    vendor_phone = db.Column(db.String(20))
    device_types = db.relationship('DeviceType')

    def __init__(self, name, contact, phone):
        self.vendor_name = name
        self.vendor_contact = contact
        self.vendor_phone = phone

#设备型号
class DeviceType(db.Model):
    dev_typeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dev_type = db.Column(db.String(40), unique=True)
    dev_class_id = db.Column(db.Integer, db.ForeignKey('device_class.dev_classid'))
    device_vendor_id = db.Column(db.Integer, db.ForeignKey('device_vendor.vendor_id'))
    device_node = db.relationship('DeviceNode', uselist=False)
    device_vendor = db.relationship('DeviceVendor', uselist=False)

    def __init__(self, new_dev_type,class_id,vendor_id):
        self.dev_type = new_dev_type
        self.dev_class_id = class_id
        self.device_vendor_id = vendor_id

#设备类型
class DeviceClass(db.Model):
    dev_classid = db.Column(db.Integer, primary_key=True)
    dev_class_desc = db.Column(db.String(40), unique=True)
    device_node = db.relationship('DeviceNode', uselist=False)
    device_type = db.relationship('DeviceType', uselist=False)

    def __init__(self, class_id, desc):
        self.dev_classid = class_id
        self.dev_class_desc = desc

#设备所在机架位置信息
class DeviceRackPos(db.Model):
    pos_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rack_id = db.Column(db.Integer, db.ForeignKey('rack.rack_id'))
    start_pos = db.Column(db.Integer, nullable=False)
    end_pos = db.Column(db.Integer, nullable=False)
    device_node = db.relationship('DeviceNode', uselist=False)
    rack = db.relationship('Rack', uselist=False)

    def __init__(self,new_rack_id,new_start_pos,new_end_pos):
        self.rack_id = new_rack_id
        self.start_pos = new_start_pos
        self.end_pos = new_end_pos

#设备节点信息
class DeviceNode(db.Model):
    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_typeid = db.Column(db.Integer, db.ForeignKey('device_type.dev_typeid'))
    device_classid = db.Column(db.Integer, db.ForeignKey('device_class.dev_classid'))
    device_alias = db.Column(db.String(40), unique=True)
    device_posid = db.Column(db.Integer, db.ForeignKey('device_rack_pos.pos_id'))
    device_proj = db.Column(db.String(40))
    device_owner = db.Column(db.String(10))
    device_contact = db.Column(db.String(20))
    device_vlan_group = db.Column(db.Integer)
    network_ports = db.relationship('NetworkPort')
    management_ips = db.relationship('ManageIP')
    device_rack_pos = db.relationship('DeviceRackPos', uselist=False)

    def __init__(self, typeid, classid, alias, posid, owner, contact, proj = "Ctyun",vlan_group = "1"):
        self.device_typeid = typeid
        self.device_classid = classid
        self.device_alias = alias
        self.device_posid = posid
        self.device_proj = proj
        self.device_owner = owner
        self.device_contact = contact
        self.device_vlan_group = vlan_group

#网络端口
class NetworkPort(db.Model):
    netport_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_device_id = db.Column(db.Integer, db.ForeignKey('device_node.device_id'))
    port_type = db.Column(db.Integer) #GE电口为1，GE光口为2，10GE光口为3，FC口为4
    parent_device = db.relationship('DeviceNode', uselist=False)

#网络网线链接
class NetworkWire(db.Model):
    net_wireid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_port_id = db.Column(db.Integer)
    dest_port_id = db.Column(db.Integer)

#网络设备管理IP
class ManageIP(db.Model):
    ip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_device_id = db.Column(db.Integer, db.ForeignKey('device_node.device_id'))
    ip_address = db.Column(db.String(20))
    is_primary = db.Column(db.Boolean)
    parent_device = db.relationship('DeviceNode', uselist=False)

#公网私网IP映射信息
class PublicIP(db.Model):
    public_ip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_ip = db.Column(db.String(20))
    private_ip = db.Column(db.String(20))

class VLANInfo(db.Model):
    vlan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vlan_group_no = db.Column(db.Integer)
    vlan_no = db.Column(db.Integer)

def init_db_data():
    #drop and regenerate the tables:
    db.drop_all()
    db.create_all()
    #init the device type databse
    db.session.add(DeviceClass(1, u"交换机"))
    db.session.add(DeviceClass(2, u"服务器"))
    db.session.add(DeviceClass(3, u"防火墙"))
    db.session.add(DeviceClass(4, u"负载均衡"))
    db.session.add(DeviceClass(5, u"刀框"))
    db.session.add(DeviceClass(6, u"磁盘阵列"))
    db.session.commit()

    dev_node = DeviceNode()
    dev_node.device_classid = 3
    db.session.add(dev_node)
    db.session.commit()
    class_id = DeviceNode.query.get(1).device_classid
    print DeviceClass.query.get(class_id).dev_class_desc

    zone = Zone(u"D座1楼机房")
    zone.add_rack(Rack(u"A-1", u"第一排第二个"))
    db.session.add(zone)
    db.session.commit()
    rack = Rack.query.get(1)
    print rack.rack_name

    vendor1=DeviceVendor(u"戴尔",u"张三","138128121")
    db.session.add(vendor1)
    db.session.commit()
    vendor_id = DeviceVendor.query.get(1).vendor_id
    print DeviceVendor.query.get(vendor_id).vendor_name

if __name__ == '__main__':
    print app.config['SQLALCHEMY_DATABASE_URI']
    init_db_data()
    print "database init completed!"
