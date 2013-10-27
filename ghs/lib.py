from flask import url_for, session, g, current_app, request, flash

from . import db, github, app
from .models import User

import sys
import mongoengine

def catch_error_graceful(form=None, flash=False):
    """ This is a utility function that handles exceptions that might be omitted
    from Mongoengine in a graceful, patterned way. In production these errors
    should never really happen, so they can be handled uniformly logging and user
    return. It is called by the safe_save utility. """
    # grab current exception information
    exc, txt, tb = sys.exc_info()

    def log(msg):
        from pprint import pformat
        from traceback import format_exc
        current_app.logger.warn(
            "=============================================================\n" +
            "{0}\nRequest dump: {1}\n{2}\n".format(msg, pformat(vars(request)), format_exc()) +
            "=============================================================\n"
        )

    # default to danger....
    cat = "danger"
    if exc is mongoengine.errors.ValidationError:
        msg = ('A database schema validation error has occurred. This has been'
               ' logged with a high priority.')
        log("A validation occurred.")
    elif exc is mongoengine.errors.InvalidQueryError:
        msg = ('A database schema validation error has occurred. This has been '
               'logged with a high priority.')
        log("An inconsistency in the models was detected")
    elif exc is mongoengine.errors.NotUniqueError:
        msg = ('A duplication error happended on the datastore side, one of '
               'your values is not unique. This has been logged.')
        log("A duplicate check on the database side was not caught")
    elif exc in (mongoengine.errors.OperationError, mongoengine.errors.DoesNotExist):
        msg = 'An unknown database error. This has been logged.'
        log("An unknown operation error occurred")
    else:
        msg = 'An unknown error has occurred'
        log("")

    if form:
        form.start.add_msg(message=msg, type=cat)
    elif flash:
        flash(msg, category=cat)
