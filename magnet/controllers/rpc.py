from datetime import date, datetime
from xmlrpc.client import dumps, loads
import xmlrpc.client

from werkzeug.wrappers import Response

from odoo.http import Controller, dispatch_rpc, request, route
from odoo.service import wsgi_server
from odoo.fields import Date, Datetime

from odoo.addons.base.controllers.rpc import RPC

class magnetRPC(RPC):
    """Handle RPC connections."""

    def _xmlrpc(self, service):
        """Common method to handle an XML-RPC request."""
        data = request.httprequest.get_data()
        params, method = loads(data)
        result = dispatch_rpc(service, method, params)
        return dumps((result,), methodresponse=1, allow_none=False)

    @route("/xmlrpc/<service>", auth="none", methods=["POST"], csrf=False, save_session=False, cors='*')
    def xmlrpc_1(self, service):
        """XML-RPC service that returns faultCode as strings.

        This entrypoint is historical and non-compliant, but kept for
        backwards-compatibility.
        """
        try:
            response = self._xmlrpc(service)
        except Exception as error:
            response = wsgi_server.xmlrpc_handle_exception_string(error)
        return Response(response=response, mimetype='text/xml')

    @route("/xmlrpc/2/<service>", auth="none", methods=["POST", "GET", "OPTIONS"], csrf=False, save_session=False, cors='*')
    def xmlrpc_2(self, service):
        """XML-RPC service that returns faultCode as int."""
        try:
            response = self._xmlrpc(service)
        except Exception as error:
            response = wsgi_server.xmlrpc_handle_exception_int(error)
        return Response(response=response, mimetype='text/xml')

    @route('/jsonrpc', type='json', auth="none", save_session=False, cors='*')
    def jsonrpc(self, service, method, args):
        """ Method used by client APIs to contact OpenERP. """
        return dispatch_rpc(service, method, args)
