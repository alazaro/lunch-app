# -*- coding: utf-8 -*-
"""
Flask app initialization.
"""
# pylint: disable=invalid-name, unused-variable, unused-import
from flask import Flask, g

from flask.ext import restful, login
from flask.ext.admin import Admin
from flask.ext.login import LoginManager, current_user
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

from raven.contrib.flask import Sentry

from social.apps.flask_app.default.models import init_social
from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.template_filters import backends

from werkzeug.exceptions import default_exceptions
from .utils import error_handler


def init_social_login():
    """
    Init login with Google OAuth2.
    """
    app.register_blueprint(social_auth)
    init_social(app, db)

    login_manager = login.LoginManager()
    login_manager.login_view = 'index'
    login_manager.login_message = ''
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        """
        Get User object.
        """
        from . import models
        try:
            return models.User.query.get(userid)
        except (TypeError, ValueError):
            pass

    @app.before_request
    def global_user():
        """
        Save User object in globals so it can be easily accessed.
        """
        g.user = login.current_user

    @app.context_processor
    def inject_user():
        """
        Save User object so it can be easily accessed in templates.
        """
        try:
            return {'user': g.user}
        except AttributeError:
            return {'user': None}

    app.context_processor(backends)


def init_api():
    """
    Expose resources via API.
    """
    from . import resources
    api.add_resource(resources.Order, '/api/v1/order')


def init_admin():
    """
    Expose some of models in Admin.
    """
    from . import models
    from .permissions import AdminModelViewWithAuth
    admin.add_view(AdminModelViewWithAuth(models.User, db.session))
    admin.add_view(AdminModelViewWithAuth(models.Order, db.session))
    admin.add_view(AdminModelViewWithAuth(models.Food, db.session))
    admin.add_view(AdminModelViewWithAuth(models.Finance, db.session))
    admin.add_view(AdminModelViewWithAuth(models.MailText, db.session))
    admin.add_view(AdminModelViewWithAuth(models.Company, db.session))


def init():
    """
    Configure some elements of application.
    Function should be called after configuration was loaded from file.
    """
    db.app = app
    db.init_app(app)
    init_social_login()
    init_api()
    init_admin()
    mail.init_app(app)

    for exception in default_exceptions:
        app.register_error_handler(exception, error_handler)

    app.register_error_handler(Exception, error_handler)


app = Flask(__name__)
db = SQLAlchemy()
admin = Admin(app)
api = restful.Api(app)
migrate = Migrate(app, db)
mail = Mail()
sentry = Sentry(app)
