#!/usr/bin/python
# -*- coding: utf-8 -*-

from db_modules import Rack,DeviceClass,DeviceNode,DeviceType,DeviceRackPos,NetworkPort,Zone
from db_modules import ManageIP,PublicIP,VLANInfo
from flask import Blueprint,render_template
from appenv import db

instdev_page = Blueprint('instdev_page', __name__)


@instdev_page.route('/')
def instdev_index():
    index = instdev_root()
    return render_template('instdev/instdev.html', bind_data=index.get_index_bind())

class instdev_root:
    def get_index_bind(self):
        bind_data = {}

#        device_type_list = [{"key": "dl360", "value": "HP DL380G8"}, {"key": "dl380", "value": "HP DL360G7"},
#                            {"key": "s5500", "value": "H3C S5500"}, {"key": "s7606", "value": "Dell R720"}]
        device_type_list = DeviceType.query.all()
        bind_data["device_type"] = device_type_list

#        device_class_list = [{"key": "switch", "value": u"交换机"}, {"key": "router", "value": u"路由器"},
#                             {"key": "rack", "value": u"机架服务器"}, {"key": "blade", "value": u"刀框"}]
        device_class_list = DeviceClass.query.all()
        bind_data["device_class"] = device_class_list

#        rackpos_list = [{"key": "d-1", "value": u"D座1号机架"}, {"key": "d-2", "value": u"D座2号机架"},
#                        {"key": "d-3", "value": u"D座3号机架"}, {"key": "d-4", "value": u"D座4号机架"}]
        rackpos_list = Rack.query.all()
        bind_data["rack_pos"] = rackpos_list

#        zone_list = [{"key": "d-1", "value": u"D座1楼机房"}, {"key": "e-2", "value": u"E座2楼机房"}]
        zone_list = Zone.query.all()
        bind_data["rack_zone"] = zone_list

#        假数据, 已执行，在数据库中
#        pos = DeviceRackPos(4,26,28) #添加一个设备位置
#        db.session.add(pos)
#        db.session.commit()
#        node1 = DeviceNode(3,1,"show",1,u"陈龙",18911890828) #在上述位置添加设备
#        db.session.add(node1)
#        db.session.commit()
#        print(db.session.query(DeviceRackPos).get(1).start_pos)
#        print(db.session.query(DeviceRackPos).get(1).end_pos)
#        print(db.session.query(DeviceNode).get(1).device_owner)
#        db.session.query(DeviceNode).get(1).device_alias = "cdn-1"
#        db.session.query(DeviceNode).get(1).device_typeid = 5
#        db.session.query(DeviceNode).get(1).device_classid = 2
#        db.session.query(DeviceNode).get(1).device_rack_pos = db.session.query(DeviceRackPos).get(3)
#        db.session.commit()

        device_list = [{"key": "hadoop-1", "value": u"Hadoop1"}, {"key": "hadoop-2", "value": u"Hadoop2"}]
        bind_data["device_list"] = device_list

        dev_port_list = [{"key": "1", "value": u"Port-A"}, {"key": "2", "value": u"Port-B"}]
        bind_data["dev_port_list"] = dev_port_list

        return bind_data