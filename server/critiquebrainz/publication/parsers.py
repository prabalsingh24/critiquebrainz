from flask import request
from critiquebrainz.utils import validate_uuid
from critiquebrainz.exceptions import *
from critiquebrainz.db import Publication

# json/query
def parse_release_group_param(source='query'):
    if source == 'query':
        release_group = request.args.get('release_group', None)
    elif source == 'json':
        release_group = request.json.get('release_group', None)
    if release_group is not None and not validate_uuid(release_group):
        raise InvalidRequest('Parameter `release_group` not valid')
    return release_group

# json
def parse_text_param(min, max):
    text = request.json.get('text', None)
    if text is None:
        raise InvalidRequest('Parameter `text` is missing')
    text_len = len(text)
    if text_len < min:
        raise InvalidRequest('Parameter `text` is too short (min=%d)' % min)
    if text_len > max:
        raise InvalidRequest('Parameter `text` is too long (max=%d)' % max)
    return text

# query
def parse_user_id_param():
    user_id = request.args.get('user_id', None)
    if user_id is not None and not validate_uuid(user_id):
        raise InvalidRequest('Parameter `user_id` not valid')
    return user_id
    
def parse_include_param():
    include = request.args.get('inc')
    if include:
        includes = include.split()
        for include in includes:
            if include not in Publication.allowed_includes:
                raise InvalidRequest('Parameter `include` not valid')
        return includes
    else:
        return None

def parse_limit_param(default, min, max):
    limit = request.args.get('limit')
    if limit is None:
        return default

    if limit.isdigit() is False:
        raise InvalidRequest('Parameter `limit` is NaN')

    limit = int(limit)
    if limit not in range(min, max+1):
        raise InvalidRequest('Parameter `limit` should be between %d and %d' \
            '(default %d)' % (min, max, default))
    return limit

def parse_offset_param(default):
    offset = request.args.get('offset')
    if offset is None:
        return default

    if offset.isdigit() is False:
        raise InvalidRequest('Parameter `offset` is NaN')
    offset = int(offset)
    return offset

def parse_rating_param(default):
    rating = request.args.get('rating')
    if rating is None:
        return default

    if rating.isdigit() is False:
        raise InvalidRequest('Parameter `rating` is NaN')

    rating = int(rating)
    if rating not in [-1, 0, 1, 2, 3]:
        raise InvalidRequest('Parameter `rating` should be between -1 and 3 '\
            '(default %d)' % default)

    return rating
