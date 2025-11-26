import socket
import argparse


def socket_connection(hostname, port, data):
    with socket.socket() as client_socket:
        address = (hostname, port)

        client_socket.connect(address)
        client_socket.send(data.encode())

        response = client_socket.recv(1024)
        response = response.decode()
        print(response)

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
    parser.add_argument(
        "data",
        type=str
    )

    args = parser.parse_args()
    socket_connection(args.hostname, args.port, args.data)


if __name__ == "__main__":
    main()

