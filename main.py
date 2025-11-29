import socket
import argparse
import itertools
import string


def bruteforce(client_socket):
    characters = string.ascii_lowercase + string.digits
    max_attempts = 1000000
    try_count = 0
    for length in range(1, len(characters)+1):
        password_iter = itertools.product(characters, repeat=length)
        for password in password_iter:
            if try_count >= max_attempts:
                return
            data = "".join(password)
            client_socket.send(data.encode())

            response = client_socket.recv(1024)
            response = response.decode()

            if response == "Connection success!":
                print(data)
                return
            try_count += 1

def connection(hostname, port):
    with socket.socket() as client_socket:
        address = (hostname, port)

        client_socket.connect(address)
        bruteforce(client_socket)


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
