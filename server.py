import socket
import select
import queue
import os


def run_server():
    host = ''
    port = 8888

    # create a TCP socket
    tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("TCP socket created")
    tcp_s.setblocking(0)            # to set the socket as non-blocking
    tcp_s.bind((host, port))            # bind to port 8888
    tcp_s.listen(5)
    print("TCP server is ready to receive")

    # create a UDP socket
    udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP socket created")
    udp_s.setblocking(0)                # to set the socket as non-blocking
    udp_s.bind((host, port))            # bind to port 8888
    print("UDP server is ready to receive")

    sockets = [tcp_s, udp_s]            # sockets to read from

    outputs = []                        # sockets to write to

    out_messages = {}                   # a que that contains outgoing messages
    # try:
    while True:
        read, write, exception = select.select(sockets, outputs, sockets)

        for i in read:
            if i is tcp_s:          # detecting a new tcp connection
                connectionSocket, addr = i.accept()
                print("Accepted a TCP connection from", addr[0])
                # set it so that it is non-blocking
                connectionSocket.setblocking(0)
                # add new client socket to monitor
                sockets.append(connectionSocket)

                # create a queue for the new connection
                out_messages[connectionSocket] = queue.Queue()

            elif i is udp_s:                            # Detecting a message from a udp client
                message, addr = i.recvfrom(1024)
                message = message.decode()
                print("UDP Client:", message)
                # Send response back to client
                i.sendto(bytes(message, "utf-8"), addr)

            else:
                message = i.recv(1024).decode()
                if message:                             # A readable channel has data
                    print("TCP Client:", message)

                    if i not in outputs:                # Add an output channel for the response
                        outputs.append(i)

                    if message == "list":
                        file_list = ""
                        for f in os.listdir('.'):
                            file_list = file_list + f + '\n'
                        out_messages[i].put(file_list.rstrip('\n'))

                    elif message[:3] == "get":
                        temp = get_file(message[4:len(message)])
                        out_messages[i].put(temp)

                    elif message == "logout":
                        print("Closing connection with", addr[0])
                        # Close connection with socket i
                        if i in outputs:
                            outputs.remove(i)
                        # Remove i from the sockets monitored
                        sockets.remove(i)
                        i.close()               # Close socket

                        del out_messages[i]

                    # elif message == "terminate":
                    #     terminate(read, sockets, outputs, out_messages)

                    else:
                        message = "Unknown command: " + message
                        out_messages[i].put(message)

        for i in write:
            try:
                nxt_output = out_messages[i].get_nowait()
            except queue.Empty:
                outputs.remove(i)
            else:
                i.sendall(bytes(nxt_output, "utf-8"))
    # except:
    #     print("An Error Occured!")

    # finally:
    #     for i in sockets:
    #         sockets.remove(i)
    #         outputs.remove(i)
    #     i.shutdown(socket.SHUT_RDWR)
    #     i.close
    #     del out_messages[i]


# def terminate(read, sockets, outputs, out_messages):
#     for i in sockets:
#         sockets.remove(i)
#         outputs.remove(i)
#     i.shutdown(socket.SHUT_RDWR)
#     i.close
#     del out_messages[i]

def get_file(file_name):
    print("Open file:", file_name)


if __name__ == "__main__":
    run_server()
