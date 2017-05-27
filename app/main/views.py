from datetime import datetime
from flask import render_template, redirect, url_for, jsonify, request
from . import main, report
from .. import db
from .forms import HostForm
from ..models import Hosts


@main.route('/', methods=['GET', 'POST'])
def index():
    form = HostForm()
    hosts = Hosts.query.order_by(Hosts.status.asc()).all()
    if len(hosts) == 0:
        now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        perc_up = 0
    else:
        now = hosts[0].last_checked
        if now is not None:
            now = datetime.strftime(now, '%m/%d/%Y %H:%M:%S')
        else:
            now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        total_hosts = len(hosts)
        up_hosts = len(Hosts.query.filter_by(status=True).all())
        perc_up = up_hosts / total_hosts
        perc_up = float("%.2f" % perc_up)
    if form.validate_on_submit():
        if len(form.port.data) == 0:
            port = None
        else:
            port = form.port.data
        host_data = (form.fqdn.data, port)
        status, timestamp = report.check_host(host_data)
        host = Hosts(fqdn=form.fqdn.data, port=port, friendly_name=form.friendly_name.data,
                     status=status, last_checked=timestamp)
        db.session.add(host)
        return redirect(url_for('main.index'))
    
    return render_template('index.html', hosts=hosts, percent_up=perc_up, timestamp=now, form=form)


@main.route('/check-hosts', methods=['GET', 'POST'])
def check_hosts():
    hosts = Hosts.query.all()
    if request.method == 'POST':
        if len(hosts) == 0:
            return jsonify({}, 204)
        report.check_hosts()
        return jsonify({}, 202)
    else:
        if len(hosts) == 0:
            return redirect(url_for('main.index'))
        report.check_hosts()
    return redirect(url_for('main.index'))
