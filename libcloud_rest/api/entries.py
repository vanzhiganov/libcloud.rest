# -*- coding:utf-8 -*-
from libcloud_rest.exception import NoSuchObjectError
from libcloud_rest.api import validators as valid


class BasicEntry(object):
    render_attrs = []  # list of object attributes which added to json
    #list of attributes and their types which required to create object
    arguments = {}  # type: validator

    @classmethod
    def to_json(cls, obj):
        return dict(
            ((a_name, getattr(obj, a_name)) for a_name in cls.render_attrs)
        )

    @classmethod
    def validate_input_json(cls, params):
        args = {}
        for name, validator in cls.arguments.iteritems():
            data = params.get(name, None)
            if validator.required or (data is not None):
                validator(data)
                args[name] = data
        return args

    @classmethod
    def _get_object(cls, arguments, driver):
        pass

    @classmethod
    def from_json(cls, params, driver=None):
        args = cls.validate_input_json(params)
        return cls._get_object(args, driver)


class NodeEntry(BasicEntry):
    render_attrs = ['id', 'name', 'state', 'public_ips']
    arguments = {'node_id': valid.StringValidator()}

    @classmethod
    def _get_object(cls, arguments, driver):
        nodes_list = driver.list_nodes()
        node_id = arguments['node_id']
        for node in nodes_list:
            if node_id == node.id:
                return node
        raise NoSuchObjectError(obj_type='Node')


class ZoneEntry(BasicEntry):
    render_attrs = ['id', 'domain', 'type', 'ttl']
    arguments = {'zone_id': valid.StringValidator()}

    @classmethod
    def _get_object(cls, driver, arguments):
        zone_id = arguments['zone_id']
        return driver.get_zone(zone_id)


class ZoneIDEntry(BasicEntry):
    render_attrs = ['zone_id']
    arguments = {'zone_id': valid.StringValidator()}

    @classmethod
    def _get_object(cls, arguments, driver=None):
        zone_id = arguments['zone_id']
        return type('ZoneID', (), {'zone_id': zone_id})


LIBCLOUD_TYPES_ENTRIES = {
    'L{Node}': NodeEntry,
    'L{Zone}': ZoneEntry,
    'zone_id': ZoneIDEntry,
}