from flask import url_for, session, g, current_app, flash

from . import db, github

import cryptacular.bcrypt
import datetime
import mongoengine
import re
import werkzeug
import json

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

class CommonMixin(object):
    """ mixin for all documents in database. provides some nice utils"""
    def safe_save(self, **kwargs):
        try:
            self.save(**kwargs)
        except Exception:
            catch_error_graceful(form)
            return False
        else:
            return True
        return True

    def jsonize(self, **kwargs):
        for key, val in kwargs.items():
            try:
                attr = getattr(self, key)
                if isinstance(attr, db.Document):
                    attr = str(attr.id)
                elif isinstance(attr, bool):
                    pass
                else:
                    attr = str(attr)
            except AttributeError:
                pass
            else:
                kwargs[key] = attr
        return json.dumps(kwargs)

    meta = {'allow_inheritance': True}

class Email(db.EmbeddedDocument):
    address = db.StringField(max_length=1023, required=True, unique=True)
    verified = db.BooleanField(default=False)
    primary = db.BooleanField(default=True)


class User(db.Document, CommonMixin):
    # _id
    username = db.StringField(max_length=32, min_length=3, primary_key=True)

    # User information
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    _password = db.StringField(max_length=128, min_length=5, required=True)
    emails = db.ListField(db.EmbeddedDocumentField('Email'))

    # Github sync
    gh_token = db.StringField()

    meta = {'indexes': [{'fields': ['gh_token'], 'unique': True, 'sparse': True}]}

    @property
    def password(self):
        return self._password

    @property
    def gh_linked(self):
        return bool(self.gh_token)

    @password.setter
    def password(self, val):
        self._password = unicode(crypt.encode(val))

    def check_password(self, password):
        return crypt.check(self._password, password)

    @property
    def gh(self):
        if 'github_user' not in session:
            session['github_user'] = github.get('user').data
        return session['github_user']

    def gh_repos(self):
        """ Generate a complete list of repositories """
        try:
            return github.get('user/repos').data
        except ValueError:
            self.gh_deauth()

    def gh_deauth(self, flatten=False):
        """ De-authenticates a user and redirects them to their account
        settings with a flash """
        flash("Your GitHub Authentication token was missing when expected, please re-authenticate.")
        self.gh_token = ''
        for project in self.get_projects():
            project.gh_desync(flatten=flatten)

    def gh_repos_syncable(self):
        """ Generate a list only of repositories that can be synced """
        for repo in self.gh_repos():
            if repo['permissions']['admin']:
                yield repo
    def gh_repo(self, path):
        """ Get a single repositories information from the gh_path """
        return github.get('repos/{0}'.format(path)).data

    @property
    def primary_email(self):
        for email in self.emails:
            if email.primary:
                return email

    @classmethod
    def create_user(cls, username, password, email_address):
        try:
            email = Email(address=email_address)
            user = cls(emails=[email], username=username)
            user.password = password
            user.save()
        except Exception:
            catch_error_graceful()

        return user

    @classmethod
    def create_user_github(cls, access_token):
        user = cls(gh_token=access_token)
        try:
            email = Email(address=user.gh['email'])
            user.save()
        except mongoengine.errors.OperationError:
            return False

        return user

    def get_abs_url(self):
        return url_for('main.user', username=unicode(self.username).encode('utf-8'))

    def get_projects(self):
        return Project.objects(maintainer=self)

    def save(self):
        self.username = self.username.lower()
        super(User, self).save()

    # Authentication callbacks
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)

    def __str__(self):
        return self.username

    # Convenience functions
    def __repr__(self):
        return '<User %r>' % (self.username)

    def __eq__(self, other):
        """ This returns the actual user object compaison when it's a proxy object.
        Very useful since we do this for auth checks all the time """
        if isinstance(other, werkzeug.local.LocalProxy):
            return self == other._get_current_object()
        else:
            return super(User, self).__eq__(other)


from .lib import (catch_error_graceful)
