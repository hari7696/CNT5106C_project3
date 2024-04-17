# ChatApp

This is a command-line-based chat application developed in Python, utilizing sockets and threading for functionality. It enables users to communicate by sending messages and sharing files with another user on the same network.

### Requirements
* Python 3.x

### Usage Instructions
1. Open a terminal window.
2. Navigate to the folder containing the ChatApp code.
3. Execute the command: `python chat.py <user_name>`
4. The program will ask you to input a port number. Type in the port number corresponding to the user you want to connect with.
5. You can start messaging by typing your messages and hitting enter to send them.
6. To send a file, enter `transfer <file_path>` and hit enter. The file will be transferred if it is found in the specified path.

### Operational Details
The ChatApp class leverages Python’s socket and threading modules to establish server and client sockets that facilitate user communication on the same network. Upon launching the app, it creates a socket bound to a random port on the localhost and prompts the user to enter the port number of the user they intend to connect with. Communication is enabled once the connection is established. Users can send messages and initiate file transfers by typing `transfer <file_path>`. File sharing is supported through binary file I/O, alongside the use of socket’s `sendall()` and `recv()` methods.

### Acknowledgements
The application was programmed by Hari and Avinash.