from django.http import HttpResponse
import datetime
import json
from django.template.response import TemplateResponse
import random
import os
from game.errors import ChallengeError
from django.db import connections

def json_custom_parser(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        dot_ix = 19
        return obj.isoformat()[:dot_ix]
    else:
        raise TypeError(obj)

def start_hack(request):
    return TemplateResponse(request, 'sql_inject_auth_code.html', context={})

def submit_attempt(request):
    try:
        results = _submit_test(request.POST)
        return HttpResponse(json.dumps(results, default=json_custom_parser), content_type='application/json', status=200)
    except ChallengeError as e:
        return HttpResponse(json.dumps(e.serialize(), default=json_custom_parser), content_type='application/json', status=400)

def _submit_test(post_data):
    auth_code = post_data['auth_code']

    challenge_meta = {}
    challenge_meta['query'] = "SELECT name,last_login from game_authcode WHERE code='{auth_code}'"
    #challenge_meta['query'] = "SELECT name,last_login from game_authcodenum WHERE code={auth_code}"

    #20 total potential filters, some duplicated
    possible_filters = ['"', "/", "\\", " ", "and", "or", "where", "limit", "null", "union", "select", "from", "having", "&", "=", "|", "union", "select", " "]
    if "game_authcodenum" in challenge_meta['query']:
        possible_filters.append("'")
    else: #game_authcode
        #escaping single quotes for game_authcode removes sql injection
        possible_filters.append('"')

    random.shuffle(possible_filters)

    #Filter out certain strings, more as difficulty increases
    challenge_meta['filters'] = []
    for i in range(0):
        challenge_meta['filters'].append(possible_filters[i])

    for filt in challenge_meta['filters']:
        auth_code = auth_code.replace(filt, '')

    print "Filters active:", challenge_meta['filters']

    query = challenge_meta['query'].replace("{auth_code}", auth_code)
    print "Query attempt:", query

    try:
        cursor = connections['default'].cursor()
        cursor.execute(query)
        keys = [col[0] for col in cursor.description]
        results = [
            dict(zip(keys, row))
            for row in cursor.fetchall()
        ]

        match_found = False
        name = ""
        last_login = ""
        ctf_flag = ''
        if len(results) > 0:
            for r in results:
                if r.get('name') and r.get('last_login'):
                    print "SUCCESS with query", query, challenge_meta['filters']
                    ctf_flag = os.environ.get('CTF_FLAG')
                    match_found = True
                    name = r.get('name')
                    last_login = r.get('last_login')

    except Exception as e:
        print "submit_attempt error", str(e)

        raise ChallengeError(query, etype="Invalid Syntax")

    finally:
        cursor.close()


    return {
        'ctf_flag': ctf_flag,
        "match_found": match_found,
        "name": name,
        "last_login": last_login
    }
