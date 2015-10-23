
from requests import Request, Session, get

from flask import Blueprint, render_template, request
from flask_login import login_required

from ..auth.views import generate_auth_header
from .. import app

SERVICES_ENDPOINT = app.config['PUB_URL']
# should requests verify the certificates for ssl connections
VERIFY_CERT = app.config['VERIFY_CERT']


manager = Blueprint('manager', __name__,
                    template_folder='templates',
                    static_folder='static')


@manager.route('/')
@login_required
def show_app(path=None):
    return render_template('manager/manager.html')


@manager.route('/services/<op>/')
def services_proxy(op):
    url = '%s%s/' % (SERVICES_ENDPOINT, op)
    headers = generate_auth_header(request)

    proxy_request = Request(method=request.method,
                            url=url,
                            headers=headers,
                            data=request.data)
    resp = Session().send(proxy_request.prepare(), verify=VERIFY_CERT)

    return (resp.text, resp.status_code, resp.headers.items())


@manager.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404