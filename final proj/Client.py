'''
Audrey Chang, Grace Jun
5/20/24

-define functions and attributes w/in server class
    -_init_
            -creates client socket with user entering server IP or hostname and port
            
    - create_connection()
            - connection to the server should be established
            - once connection is established b/w client/server, ask user to enter username and send it to server

    -message_handling()
            -prints messages received from other users (sent via server)

    -input_handling()
            -sends user messages formatted with their username concatenated to the server
            
    - close_connection()
            - close the socket connection and exit the program if needed.
            - use this when the user decides to exit or the connection is terminated on errors

    **use threading library to allow multiple subprocesses to run simultaneously
'''
import threading
import socket

class Client_Socket():

    def __init__(self, server_IP, port):
        self.client_socket = None
        self.username = None
        self.create_connection(server_IP, port)

    def create_connection(self, server_IP, port):
        try:
            #creates client socket with user entering server IP or hostname and port
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_IP, port))

            #a connection to the server should be established after ^^
            # once connection is established ask user to enter username and send it to server
            self.username = input("Please enter your username: ")
            self.client_socket.send(self.username.encode('utf-8'))

            # start message handling thread
            message_thread = threading.Thread(target=self.message_handling)
            message_thread.start()
            # Keep the main thread running while other threads are active
            input_thread = threading.Thread(target=self.input_handling)
            input_thread.start()

        except Exception as e:
            print(f"Connection error: {str(e)}")
            self.close_connection()

    def message_handling(self):
        while True:
            try:
                # print welcome message from server
                data = self.client_socket.recv(1024)
                if data:
                    print(data.decode('utf-8'))
                else:
                # If no data is received, the server needs to close connection
                    print("Disconnected from server.")
                    self.close_connection()
                    break
            except Exception as e:
                print(f"Error handling message: {str(e)}")
                self.close_connection()
                break
    
    def input_handling(self):
        while True:
            try:
                message = input()
                self.client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {str(e)}")
                self.close_connection()
                break

    def close_connection(self):
        try:
            if self.client_socket:
                self.client_socket.close()
        except Exception as e:
            print(f"Error Closing Connection: {str(e)}")
        finally:
            print("Connection Closed.")
            exit(0)
        

if __name__ == '__main__':
    try:
        client = Client_Socket("127.0.0.1", 1234)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
