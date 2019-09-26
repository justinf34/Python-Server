import socket
import argparse
import errno


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'server_ip', help="Server of ip you are trying to connect to", type=str)
    parser.add_argument('port_num', help="Port number of server", type=int)

    return parser.parse_args()


def main():
    args = parse_args()

    serverName = args.server_ip
    serverPort = args.port_num
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientSocket.connect((serverName, serverPort))
        print("Connected to", serverName)

        while 1:
            message = input(
                "Please enter a message to be sent to the server ('logout' to terminate):")
            clientSocket.sendall(bytes(message, "utf-8"))

            if message == "logout" or message == "terminate":
                break

            data = clientSocket.recv(1024).decode()
            print(data)

    except socket.error as e:
        if e.errno == errno.ECONNRESET:
            print("Disconnected from", serverName)
        else:
            print(
                "An error occured connecting to, sending to, or receiving from", serverName)

    finally:
        clientSocket.close()
        print("TCP Socket closed")


if __name__ == "__main__":
    main()
