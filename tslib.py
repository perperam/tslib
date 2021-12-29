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

    def ts_command(self, command):
        self.write(f"{command}\n".encode())
        return self.feedback()

    def feedback(self):
        # test if the server has send no error back
        reply = self.read_until(self.NO_ERROR.encode(), timeout=self.TIMEOUT)
        if reply == self.NO_ERROR.encode():
            return True, None
        else:
            return False, reply



    def login(self, user, password):
        # Testing if the login is correct by catching the welcome message
        reply = self.read_until(self.WELCOME_MSG.encode(), timeout=self.TIMEOUT)
        if reply == self.WELCOME_MSG.encode():
            self.write(f"login {user} {password}\n".encode())
            # testing if "error id=0 msg=ok" is returned by the server
            done, reply = self.feedback()
            if done:
                return True, None
        return False, reply

    def login_as_admin(self, password, virtual_server=1):
        user = "serveradmin"
        done, reply = self.login(user, password)
        if not done: return False, reply
        print("try to use 1")
        self.write(f"use {virtual_server}\n".encode())
        done, reply = self.feedback()
        if not done: return False, reply
        return True, None
