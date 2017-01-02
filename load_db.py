import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'hackathon.settings'
import django
django.setup()

import names
from django.db import connections
import random

if not os.environ.get('IS_HEROKU_SERVER', False):
    os.system("dropdb sqlinjauthcode")
    os.system("createdb sqlinjauthcode")

os.system("python manage.py migrate")

insert_data = """
INSERT INTO "game_authcode" ("code", "name", "last_login") VALUES ('{auth_code}', '{name}', '2016-12-10T23:57:43.324505'::timestamp)
"""
insert_data = insert_data.replace("{auth_code}", ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(20)))
insert_data = insert_data.replace("{name}", names.get_full_name())

try:
    cursor = connections['default'].cursor()
    cursor.execute(insert_data)
finally:
    try:
        cursor.close()
    except:
        pass


insert_data = """
INSERT INTO "game_authcodenum" ("code", "name", "last_login") VALUES ({auth_code}, '{name}', '2016-12-10T23:57:43.324505'::timestamp)
"""

insert_data = insert_data.replace("{auth_code}", str(random.randint(111111,999999)))
insert_data = insert_data.replace("{name}", names.get_full_name())

try:
    cursor = connections['default'].cursor()
    cursor.execute(insert_data)
finally:
    cursor.close()