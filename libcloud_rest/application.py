# -*- coding:utf-8 -*-
from exceptions import BaseException

from werkzeug.wrappers import Request
from werkzeug.wrappers import Response
from werkzeug.exceptions import HTTPException

from libcloud_rest.exception import LibcloudRestError
from libcloud_rest.api.urls import urls
from libcloud_rest.log import logger


class LibcloudRestApp(object):
    """
    FIXME
    """
    url_map = urls

    def dispatch(self, controller, action_name, request, params):
        """

        @param controller:
        @param action_name:
        @param request:
        @param params:
        @return:
        """
        controller.request = request
        controller.params = params
        action = getattr(controller, action_name)
        try:
            retval = action()
            return retval
        except LibcloudRestError, error:
            error_json = error.to_json()
            return Response(error_json, status=error.http_code,
                mimetype='application/json')
        except BaseException, error:
            logger.debug(str(error))
            fake_error = LibcloudRestError()  # FIXME
            return Response(
                fake_error.to_json(), status=fake_error.http_status_code,
                mimetype='application/json')  # FIXME: response error generator

    def __call__(self, environ, start_response):
        request = Request(environ)
        urls = self.url_map.bind_to_environ(environ)

        try:
            logger.debug('%s - %s %s' %
                         (request.remote_addr, request.method, request.url))
            endpoint, params = urls.match()

            (controller_class, action) = endpoint
            controller = controller_class()
            response = self.dispatch(controller, action, request, params)
        except HTTPException, e:
            response = e

        return response(environ, start_response)