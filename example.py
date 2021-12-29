from tslib import ts_query
from secrets import *


with ts_query(HOST) as ts:
    ts.write(f"login serveradmin {PW}\n".encode())
    print(ts.read_until("...".encode(), timeout=2))
    ts.write("use 1\n".encode())
    print(ts.read_until("...".encode(), timeout=2))
    ts.write("serveredit virtualserver_name=TEST\n".encode())
    print(ts.read_until("...".encode(), timeout=2))

    # print(ts.login_as_admin(PW))
    # print(ts.write("virtualserver_name=TEST\n".encode()))
    # print(ts.ts_command("virtualserver_name=TEST"))
