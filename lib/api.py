from flask import request, Response, current_app

from config import API_DB_CONFIG
from lib import consts
from lib.db import get_redis_db_from_context


def set_database_connection():
    """
    This function setups up a database connection depending on the version of the API being requested.
    And is called before each request.
    :return:
    """

    try:
        groups = request.path.split('/')
        if groups is None or len(groups) < 1:
            return Response(consts.ERROR_NOT_FOUND, status=consts.HTTP_NOT_FOUND)

        version = groups[1]

        if version in API_DB_CONFIG:
            db_number = API_DB_CONFIG[version]
        else:
            raise ValueError('Unknown API Version')
        get_redis_db_from_context(db_number)

    except Exception as e:
        return Response(consts.ERROR_NOT_FOUND, status=consts.HTTP_NOT_FOUND)


def log_request_info():
    current_app.logger.debug('=' * 50)
    current_app.logger.debug('Request')
    current_app.logger.debug('Headers: %s', request.headers)
    if 'Content-Type' not in request.headers or \
            'Content-Type' in request.headers and 'gzip' not in request.headers['Content-Type']:
        current_app.logger.debug('Body: {}'.format(request.get_data()))
    else:
        current_app.logger.debug('Body: Binary Data')

    current_app.logger.debug('=' * 50)


def log_response(resp):
    current_app.logger.debug('-' * 50)
    current_app.logger.debug('Response')
    current_app.logger.debug('Headers: {}'.format(resp.headers))
    if 'Content-Encoding' not in resp.headers or \
            'Content-Encoding' in resp.headers and 'gzip' not in resp.headers['Content-Encoding']:
        current_app.logger.debug('Body: {}'.format(resp.response))
    else:
        current_app.logger.debug('Body: Binary Data')
    current_app.logger.debug('-' * 50)
    return resp