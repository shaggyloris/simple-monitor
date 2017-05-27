from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
admin = Admin(name='Device Monitor', base_template='layout.html', template_mode='bootstrap3')


class HostModelView(ModelView):
    create_modal = True
    edit_modal = True
    can_export = True
    column_editable_list = ['fqdn', 'port', 'friendly_name']
    form_excluded_columns = ['status', 'last_checked']


# Application factory for the flask application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)
    
    from .models import Hosts
    
    admin.init_app(app)
    admin.add_view(HostModelView(Hosts, db.session))
    
    # Register blueprints for different functions within the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
