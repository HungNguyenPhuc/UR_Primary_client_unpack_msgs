import socket
import multiprocessing


def receive_and_print_data(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Received:", data.decode())


def receive_commands_and_send(conn):
    while True:
        command = input("Enter command: ")
        conn.sendall(command.encode())


def main():
    # Set up the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)
    print("Waiting for connection...")

    # Accept a connection
    conn, addr = server_socket.accept()
    print("Connected by", addr)

    # Create two processes
    recv_process = multiprocessing.Process(target=receive_and_print_data, args=(conn,))
    send_process = multiprocessing.Process(
        target=receive_commands_and_send, args=(conn,)
    )

    # Start the processes
    recv_process.start()
    send_process.start()

    # Join the processes
    recv_process.join()
    send_process.join()

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
