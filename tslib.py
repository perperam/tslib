"""
AUTHOR: https://github.com/perperam
EMAIL: perperam@icatas.eu
"""
from telnetlib import Telnet

class ts_query(Telnet):
    # the standart message send by the server when connecting
    WELCOME_MSG = """TS3\n\rWelcome to the TeamSpeak 3 ServerQuery interface, type "help" for a list of commands and "help <command>" for information on a specific command.\n\r"""
    # the standart telnet port used by the teamspeak server
    TELNET_PORT = 10011
    TIMEOUT = 4
    NO_ERROR = "error id=0 msg=ok"

    # is called when crated "with a context manager" and makes it possible to
    # have the port with an standart value as keyargument
    def __init__(self, host, port=TELNET_PORT):
        Telnet.__init__(self, host, port)

    def execute(self, command):
        self.write(f"{command}\n".encode())
        return self.feedback()

    def feedback(self):
        # test if the server has send no error back
        reply = self.read_until(self.NO_ERROR.encode(), timeout=self.TIMEOUT)
        if reply[-17:] == self.NO_ERROR.encode():
            return True, reply
        # print(reply[-17:], self.NO_ERROR.encode())
        return False, reply


    def login(self, user, password):
        # Testing if the login is correct by catching the welcome message
        reply = self.read_until(self.WELCOME_MSG.encode(), timeout=self.TIMEOUT)
        if reply == self.WELCOME_MSG.encode():
            done, reply = self.execute(f"login {user} {password}")
            if done:
                return True, reply
        return False, reply

    def login_as_admin(self, password, virtual_server=1):
        user = "serveradmin"
        done, reply = self.login(user, password)
        if not done:
            return False, reply
        done, reply = self.execute(f"use {virtual_server}")
        if not done:
            return False, reply
        return True, reply

    def edit_virtualserver_name(self, name):
        return self.execute(f"serveredit virtualserver_name={name}")
