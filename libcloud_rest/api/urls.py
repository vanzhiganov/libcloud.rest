# -*- coding:utf-8 -*-
from werkzeug.routing import Map, Rule, Submount
import libcloud

from libcloud_rest.api.handlers import ApplicationHandler
from libcloud_rest.api.handlers import ComputeHandler
from libcloud_rest.api.handlers import StorageHandler
from libcloud_rest.api.handlers import LoabBalancerHandler
from libcloud_rest.api.handlers import DNSHandler
from libcloud_rest.api.versions import versions

__all__ = [
    'urls',
    ]

prefix = '/%s' % versions[libcloud.__version__]

compute_urls = Submount(prefix + '/compute/', [
    Rule('/providers', endpoint=(ComputeHandler, 'providers'),
         methods=['GET']),
    Rule('/<string:provider>/nodes', endpoint=(ComputeHandler, 'list_nodes'),
         methods=['GET']),
    ])

storage_urls = Submount(prefix + '/storage/', [
    Rule('/providers', endpoint=(StorageHandler, 'providers'),
        methods=['GET']),
    ])

loadbalancer_urls = Submount(prefix + '/loadbalancer/', [
    Rule('/providers', endpoint=(LoabBalancerHandler, 'providers'),
         methods=['GET']),
    ])

dns_urls = Submount(prefix + '/dns/', [
    Rule('/providers', endpoint=(DNSHandler, 'providers'), methods=['GET']),
    ])

urls = Map([
    Rule('/', endpoint=(ApplicationHandler, 'index'), methods=['GET']),
    compute_urls,
    storage_urls,
    loadbalancer_urls,
    dns_urls,
    ])
