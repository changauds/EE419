'''
Audrey Chang, Grace Jun
5/20/24

-define functions and attributes w/in server class
    -_init_ 
            -create tcp socket object
            -take user input for server port # and bind it to socket created
            -always LISTENING

            -print ip address and port of server once socket has been bound and is listening

    -start_server()
            -this method should accept connections from clients
            -print client IP once new client joins

            -create list to maintain all client socket objects
            -first message sent from client is their username

    -broadcast(self, user_message)
            -broadcast a client's user_mesasge to all other clients

    -cilent_handling(self, client_socket, client_address)
            -tries to receive messages from different clients
            -OPTIONAL: when client joins server for first time, broadcast its name by calling the broadcast() function

** use THREADING library to allow multiple subprocesses to run simultaneously
** use encode and decode
'''
import threading
import socket

class ServerSocket:
    def __init__(self, port_num):
        # server IP address (localhost)
        self.server_ip = "127.0.0.1"      
        #storing client socket objects
        self.clients=[]        
        #create tcp socket object
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #take user input for server port # and bind it to socket created
        self.server.bind((self.server_ip, port_num))
        #always LISTENING
        self.server.listen(0)
        #print server IP address and port once socket has been bound and listening
        print(f"Listening on {self.server_ip}:{port_num}")

    #this method should accept connections from clients
    def start_server(self):
        # continuously accept connections from clients
        while True:
            client_socket, client_address = self.server.accept()
            print(f"Accepted connection from {client_address[0]}: {client_address[1]}")
            #print client IP once new client joins
            #create list to maintain all client socket objects
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.client_handling, args=(client_socket, client_address))
            client_thread.start()
            #first message sent from cilent is their username

    def broadcast(self, user_message, sender_socket):
        #broadcast a client's user_mesasge to all other clients
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(user_message.encode('utf-8'))
                except Exception as e:
                    print(f"Error broadcasting message: {str(e)}")
                    # remove client if sending fail
                    self.clients.remove(client)

    def client_handling(self, client_socket, client_address):
        #tries to receive messages from different clients
        try:
            #receive username fom client
            username = client_socket.recv(1024).decode('utf-8')
            print(f"{client_address[0]}:{client_address[1]} is now known as {username}")
            
            #OPTIONAL: when client joins server for first time, broadcast its name by calling the broadcast() function
            self.broadcast(f"{username} has joined the chat.", client_socket)

            while True:
                # Receive messages from the client
                data = client_socket.recv(1024)
                if not data:
                    # If no data is received, the client has disconnected
                    print(f"Connection with {client_address[0]}:{client_address[1]} closed.")
                    break
                # Decode received data
                message = data.decode("utf-8")
                print(f"Received from {username}:{message}")
                # Broadcast the received message to all other clients
                self.broadcast(f"{username}: {message}", client_socket)
        except Exception as e:
            print(f"Error handling client {client_address}: {str(e)}")
        finally:
            # Ensure the client socket is closed and removed from the clients list
            client_socket.close()
            self.clients.remove(client_socket)
            # OPTIONAL: notify others that the client has left
            self.broadcast(f"{username} has left the chat.", client_socket)

if __name__ == "__main__":
    # initialize the server with the specified port number
    server =ServerSocket(1234)
    
    # start the server to accept connections
    server.start_server()
