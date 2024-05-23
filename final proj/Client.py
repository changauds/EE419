'''
Audrey Chang, Grace Kim
5/20/24

-define functions and attributes w/in server class
    -_init_
            -creates client socket with user entering server IP or hostanem and port
            -a connection to the server should be estalished after ^^
            -once connection is established b/w client/server, ask user to enter username and send it to server

    -message_handling()
            -prints messages received from other users (sent via server)

    -input_handling()
            -sends user messsages formatted with their username concatenated to the server

    **use threading library to allow multiple subprocesses to run simultaneously
'''
import threading
import socket

class Client_Socket():

    def __init__(self, server_IP, port):
        self.username = None
        #creates client socket with user entering server IP or hostanem and port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_IP, port))
        #a connection to the server should be estalished after ^^
        #once connection is established b/w client/server, ask user to enter username and send it to server
        self.username = input("Please enter your username: ")
        self.client_socket.send(self.username.encode('utf-8'))

        data = self.client_socket.recv(1024)
        print(data.decode('utf-8'))


    def message_handling(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    print(data.decode('utf-8'))
            except Exception as e:
                print(f"Error handling message: {str(e)}")
    
    def input_handling(self):
        while True:
            try:
                message = input()
                self.client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {str(e)}")

if __name__ == '__main__':
    client = Client_Socket("127.0.0.1", 1234)
    message_thread = threading.Thread(target=client.message_handling)
    input_thread = threading.Thread(target=client.input_handling)
    message_thread.start()
    input_thread.start()
