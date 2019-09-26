import socket
import argparse


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
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    keep_sending = True

    try:
        while keep_sending:
            message = input(
                "Please enter a message to be sent to the server ('logout' to terminate):")
            if message == "logout":
                keep_sending = False
            else:
                clientSocket.sendto(bytes(message, "utf-8"),
                                    (serverName, serverPort))
                message, server_addr = clientSocket.recvfrom(1024)
                message = message.decode()
                print("Server:", message)
    except socket.error:
        print("An Error occured")
    finally:
        clientSocket.close()
        print("Socket closed")


if __name__ == "__main__":
    main()
