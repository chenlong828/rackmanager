#!/usr/bin/python
# -*- coding: utf-8 -*-


from db_modules import Rack,DeviceClass,DeviceNode,DeviceType,DeviceRackPos,NetworkPort,DeviceVendor, Zone
from db_modules import ManageIP,PublicIP,VLANInfo
from flask import Blueprint,render_template,abort, request
from appenv import db

devmgr_page = Blueprint('devmgr_page', __name__)
__author__ = 'ChenLong'

allowed_target = ('device_class', 'device_type', 'device_vendor', 'rack', 'zone')

@devmgr_page.route('/')
def devmgr_index():
    return render_template('devmgr/devmgr.html')
#######################dialog########################
#device_class
@devmgr_page.route('/dialog/add/device_class')
def dlg_add_device_class():
    return render_template('devmgr/device_class_add.html')

@devmgr_page.route('/dialog/update/device_class/<class_id>')
def dlg_update_device_class(class_id):
    dev_class = DeviceClass.query.get(class_id)
    bind_data={'class_id':dev_class.dev_classid, 'class_desc':dev_class.dev_class_desc}
    return render_template('devmgr/device_class_mod.html', bind_data=bind_data)

@devmgr_page.route('/dialog/delete/device_class/<class_id>')
def dlg_delete_device_class(class_id):
    dev_class = DeviceClass.query.get(class_id)
    bind_data={'class_id':dev_class.dev_classid, 'class_desc':dev_class.dev_class_desc}
    return render_template('devmgr/device_class_del.html', bind_data=bind_data)

#device_vendor
@devmgr_page.route('/dialog/add/device_vendor')
def dlg_add_device_vendor():
    return render_template('devmgr/device_vendor_add.html')

@devmgr_page.route('/dialog/update/vendor/<vendor_id>')
def dlg_update_device_vendor(vendor_id):
    device_vendor = DeviceVendor.query.get(vendor_id)
    bind_data={'vendor_id':device_vendor.vendor_id, 'vendor_name':device_vendor.vendor_name,
               'vendor_contact':device_vendor.vendor_contact,'vendor_phone':device_vendor.vendor_phone}
    return render_template('devmgr/device_vendor_mod.html', bind_data=bind_data)

@devmgr_page.route('/dialog/delete/vendor/<vendor_id>')
def dlg_delete_vendor(vendor_id):
    device_vendor = DeviceVendor.query.get(vendor_id)
    bind_data={'vendor_id':device_vendor.vendor_id, 'vendor_name':device_vendor.vendor_name,
               'vendor_contact':device_vendor.vendor_contact,'vendor_phone':device_vendor.vendor_phone}
    return render_template('devmgr/device_vendor_del.html', bind_data=bind_data)

#device_type
@devmgr_page.route('/dialog/add/device_type')
def dlg_add_device_type():
    class_list = DeviceClass.query.all()
    vendor_list = DeviceVendor.query.all()
    bind_data = {'class_list':class_list,'vendor_list':vendor_list}
    return render_template('devmgr/device_type_add.html',bind_data=bind_data)

@devmgr_page.route('/dialog/update/device_type/<type_id>')
def dlg_update_device_type(type_id):
    dev_type = DeviceType.query.get(type_id)
    class_list = DeviceClass.query.all()
    vendor_list = DeviceVendor.query.all()
    bind_data={'type_id':dev_type.dev_typeid, 'dev_type':dev_type.dev_type,
               'class_id':dev_type.dev_class_id,'vendor_id':dev_type.device_vendor_id,
               'class_list':class_list,'vendor_list':vendor_list}
    return render_template('devmgr/device_type_mod.html', bind_data=bind_data)

@devmgr_page.route('/dialog/delete/device_type/<type_id>')
def dlg_delete_device_type(type_id):
    dev_type = DeviceType.query.get(type_id)
    bind_data={'type_id':dev_type.dev_typeid, 'dev_type':dev_type.dev_type,
               'class_id':dev_type.dev_class_id,'vendor_id':dev_type.device_vendor_id}
    return render_template('devmgr/device_type_del.html', bind_data=bind_data)

#rack
@devmgr_page.route('/dialog/add/rack')
def dlg_add_rack():
    zone_list = Zone.query.all()
    bind_data = {'zone_list':zone_list}
    return render_template('devmgr/rack_add.html',bind_data=bind_data)

@devmgr_page.route('/dialog/update/rack/<rack_id>')
def dlg_update_rack(rack_id):
    rack = Rack.query.get(rack_id)
    zone_list = Zone.query.all()
    bind_data={'rack_id':rack.rack_id, 'rack_name':rack.rack_name,
               'rack_pos':rack.rack_pos,'zone_id':rack.zone_id,
               'zone_list':zone_list}
    return render_template('devmgr/rack_mod.html', bind_data=bind_data)

@devmgr_page.route('/dialog/delete/rack/<rack_id>')
def dlg_delete_rack(rack_id):
    rack = Rack.query.get(rack_id)
    bind_data={'rack_id':rack.rack_id, 'rack_name':rack.rack_name,
               'rack_pos':rack.rack_pos,'zone_id':rack.zone_id}
    return render_template('devmgr/rack_del.html', bind_data=bind_data)

#zone
@devmgr_page.route('/dialog/add/zone')
def dlg_add_zone():
    return render_template('devmgr/zone_add.html')

@devmgr_page.route('/dialog/update/zone/<zone_id>')
def dlg_update_zone(zone_id):
    zone = Zone.query.get(zone_id)
    bind_data={'zone_id':zone.zone_id, 'zone_name':zone.zone_name,
               'zone_owner':zone.zone_owner,'zone_phone':zone.zone_phone}
    return render_template('devmgr/zone_mod.html', bind_data=bind_data)

@devmgr_page.route('/dialog/delete/zone/<zone_id>')
def dlg_delete_zone(zone_id):
    zone = Zone.query.get(zone_id)
    bind_data={'zone_id':zone.zone_id, 'zone_name':zone.zone_name,
               'zone_owner':zone.zone_owner,'zone_phone':zone.zone_phone}
    return render_template('devmgr/zone_del.html', bind_data=bind_data)

#######################action########################
#device_class
@devmgr_page.route('/action/add/device_class', methods=['POST'])
def action_add_device_class():
    if request.method == 'POST':
        is_new_id = DeviceClass.query.get(request.form['class_id'])
        if is_new_id is not None:
            return "already exist"
        is_new_class = DeviceClass.query.get(request.form['class_id'])
        if is_new_class is not None:
            return "already exist"
        new_dev_class = DeviceClass(request.form['class_id'],request.form['class_name'])
        db.session.add(new_dev_class)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/update/device_class', methods=['POST'])
def action_update_device_class():
    if request.method == 'POST':
        mod_class = DeviceClass.query.get(request.form['class_id'])
        if mod_class is None:
            return "error record"
        mod_class.dev_class_desc = request.form['class_name']
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/delete/device_class', methods=['POST'])
def action_delete_device_class():
    if request.method == 'POST':
        del_class = DeviceClass.query.get(request.form['class_id'])
        if del_class is None:
            return "error record"
        # 欲删除的种类正在被使用
        type_list = DeviceType.query.all()
        for type in type_list:
            if str(type.dev_class_id) == str(request.form['class_id']):
                return "Error! Under using"
        db.session.delete(del_class)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

#device_vendor
@devmgr_page.route('/action/add/device_vendor', methods=['POST'])
def action_add_device_vendor():
    if request.method == 'POST':
        is_new_vendor = DeviceVendor.query.get(request.form['vendor_name'])
        if is_new_vendor is not None:
            return "already exist"
        new_dev_vendor = DeviceVendor(request.form['vendor_name'],request.form['vendor_contact']
            ,request.form['vendor_phone'])
        db.session.add(new_dev_vendor)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/update/device_vendor', methods=['POST'])
def action_update_device_vendor():
    if request.method == 'POST':
        mod_vendor = DeviceVendor.query.get(request.form['vendor_id'])
        if mod_vendor is None:
            return "error record"
        mod_vendor.vendor_contact = request.form['vendor_contact']
        mod_vendor.vendor_phone = request.form['vendor_phone']
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/delete/device_vendor', methods=['POST'])
def action_delete_device_vendor():
    if request.method == 'POST':
        del_vendor = DeviceVendor.query.get(request.form['vendor_id'])
        if del_vendor is None:
            return "error record"
        # 欲删除的厂商正在被使用
        type_list = DeviceType.query.all()
        for type in type_list:
            if str(type.device_vendor_id) == str(request.form['vendor_id']):
                return "Error! Under using"
        db.session.delete(del_vendor)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

#device_type
@devmgr_page.route('/action/add/device_type', methods=['POST'])
def action_add_device_type():
    if request.method == 'POST':
        is_new_type = DeviceType.query.get(request.form['type_name'])
        if is_new_type is not None:
            return "already exist"
        new_dev_type = DeviceType(request.form['type_name'],
            request.form['type_class_id'],request.form['type_vendor_id'])
        db.session.add(new_dev_type)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/update/device_type', methods=['POST'])
def action_update_device_type():
    if request.method == 'POST':
        mod_type = DeviceType.query.get(request.form['type_id'])
        if mod_type is None:
            return "error record"
        mod_type.dev_class_id = request.form['class_id']
        mod_type.device_vendor_id = request.form['vendor_id']
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/delete/device_type', methods=['POST'])
def action_delete_device_type():
    if request.method == 'POST':
        del_type = DeviceType.query.get(request.form['type_id'])
        if del_type is None:
            return "error record"
        db.session.delete(del_type)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

#rack
@devmgr_page.route('/action/add/rack', methods=['POST'])
def action_add_rack():
    if request.method == 'POST':
        is_new_rack = Rack.query.get(request.form['rack_name'])
        if is_new_rack is not None:
            return "already exist"
        new_rack = Rack(request.form['rack_name'],
            request.form['rack_pos'],request.form['rack_zone_id'])
        db.session.add(new_rack)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/update/rack', methods=['POST'])
def action_update_rack():
    if request.method == 'POST':
        mod_rack = Rack.query.get(request.form['rack_id'])
        if mod_rack is None:
            return "error record"
        mod_rack.rack_pos = request.form['rack_pos']
        mod_rack.zone_id = request.form['rack_zone_id']
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/delete/rack', methods=['POST'])
def action_delete_rack():
    if request.method == 'POST':
        del_rack = Rack.query.get(request.form['rack_id'])
        if del_rack is None:
            return "error record"
        db.session.delete(del_rack)
        db.session.commit()
        return "ok"
    else:
        return abort(500)
#zone
@devmgr_page.route('/action/add/zone', methods=['POST'])
def action_add_device_vendor():
    if request.method == 'POST':
        is_new_zone = Zone.query.get(request.form['zone_name'])
        if is_new_zone is not None:
            return "already exist"
        new_zone = Zone(request.form['zone_name'],request.form['zone_owner']
            ,request.form['zone_phone'])
        db.session.add(new_zone)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/update/zone', methods=['POST'])
def action_update_zone():
    if request.method == 'POST':
        print request.form['zone_id']
        mod_zone = Zone.query.get(request.form['zone_id'])
        if mod_zone is None:
            return "error record"
        mod_zone.zone_name = request.form['zone_name']
        mod_zone.zone_owner = request.form['zone_owner']
        mod_zone.zone_phone = request.form['zone_phone']
        db.session.commit()
        return "ok"
    else:
        return abort(500)

@devmgr_page.route('/action/delete/zone', methods=['POST'])
def action_delete_zone():
    if request.method == 'POST':
        del_zone = Zone.query.get(request.form['zone_id'])
        if del_zone is None:
            return "error record"
        # 欲删除的机房正在被使用
        rack_list = Rack.query.all()
        for rack in rack_list:
            if str(rack.zone_id) == str(request.form['zone_id']):
                return "Error! Under using"
        db.session.delete(del_zone)
        db.session.commit()
        return "ok"
    else:
        return abort(500)

#######################grid########################
@devmgr_page.route('/grid/list/device_class')
def get_device_class_list():
    class_list = DeviceClass.query.all()
    bind_data = {'class_list':class_list}
    return render_template('devmgr/device_class_list.html', bind_data=bind_data)

@devmgr_page.route('/grid/list/device_vendor')
def get_device_vendor_list():
    vendor_list = DeviceVendor.query.all()
    bind_data = {'vendor_list':vendor_list}
    return render_template('devmgr/device_vendor_list.html', bind_data=bind_data)

@devmgr_page.route('/grid/list/device_type')
def get_device_type_list():
    type_list = DeviceType.query.all()
    class_list = DeviceClass.query.all()
    vendor_list = DeviceVendor.query.all()
    # 因为关联数组的删减操作，query生成数组下标与id不对应
    # 现以元数组两倍（可更大）大小初始化新的以dev_class_id/vendor_id为下标的数组
    new_class_list = ["0"]*2*len(class_list)
    for dev_class in class_list:
        new_class_list[dev_class.dev_classid] = dev_class.dev_class_desc
    new_vendor_list = ["0"]*2*len(vendor_list)
    for vendor in vendor_list:
        new_vendor_list[vendor.vendor_id] = vendor.vendor_name
    bind_data = {'type_list':type_list, 'class_list':new_class_list,'vendor_list':new_vendor_list}
    return render_template('devmgr/device_type_list.html', bind_data=bind_data)

@devmgr_page.route('/grid/list/device_node')
def get_device_node_list():
    node_list = DeviceNode.query.all()
    type_list = DeviceType.query.all()
    class_list = DeviceClass.query.all()
    rack_list = Rack.query.all()
    zone_list = Zone.query.all()
    pos_list = DeviceRackPos.query.all()
    # 因为关联数组的删减操作，query生成数组下标与id不对应
    # 现以元数组两倍（可更大）大小初始化新的以dev_class_id/vendor_id为下标的数组
    new_type_list = ["0"]*10*len(type_list)
    for device_type in type_list:
        new_type_list[device_type.dev_typeid] = device_type.dev_type
    new_class_list = ["0"]*10*len(class_list)
    for dev_class in class_list:
        new_class_list[dev_class.dev_classid] = dev_class.dev_class_desc
    new_rack_list = ["0"]*10*len(rack_list)
    for rack in rack_list:
        new_rack_list[rack.rack_id] = rack.rack_pos
    new_zone_list = ["0"]*10*len(zone_list)
    for zone in zone_list:
        new_zone_list[zone.zone_id] = zone.zone_name
    bind_data = {'node_list':node_list,'type_list':new_type_list, 'class_list':new_class_list,
                 'rack_list':new_rack_list,'zone_list':new_zone_list,'pos_list':pos_list}
    return render_template('devmgr/device_node_list.html', bind_data=bind_data)

@devmgr_page.route('/grid/list/rack')
def get_rack_list():
    rack_list = Rack.query.all()
    zone_list = Zone.query.all()
    # 因为关联数组的删减操作，query生成数组下标与id不对应
    # 现以元数组两倍（可更大）大小初始化新的以zone_id为下标的数组，
    new_zone_list = ["0"]*10*len(zone_list)
    for zone in zone_list:
        new_zone_list[zone.zone_id] = zone.zone_name
    bind_data = {'rack_list':rack_list,'zone_list':new_zone_list}
    return render_template('devmgr/rack_list.html', bind_data=bind_data)

@devmgr_page.route('/grid/list/zone')
def get_zone_list():
    zone_list = Zone.query.all()
    bind_data = {'zone_list':zone_list}
    return render_template('devmgr/zone_list.html', bind_data=bind_data)

