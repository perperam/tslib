from tslib import ts_query
from secrets import *

with ts_query(HOST) as ts:
    print(ts.login_as_admin(PW))
    print(ts.edit_virtualserver_name("TEST11"))
    print("OK")
    _, reply = ts.execute("help")
    print(reply.decode())
