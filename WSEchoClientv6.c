// CS 2690 Program 1 
// Simple Windows Sockets Echo Client (IPv6)
// Last update: 2/12/19
// Rylan Cunningham 601 10/12/2024
// Windows 11 VS Community 2022
//
// Usage: WSEchoClientv6 <server IPv6 address> <server port> <"message to echo">
// Companion server is WSEchoServerv6
// Server usage: WSEchoServerv6 5000
//
// This program is coded in conventional C programming style, with the 
// exception of the C++ style comments.
//
// I declare that the following source code was written by me or provided
// by the instructor. I understand that copying source code from any other 
// source or posting solutions to programming assignments (code) on public
// Internet sites constitutes cheating, and that I will receive a zero 
// on this project if I violate this policy.
// ----------------------------------------------------------------------------

// Minimum required header files for C Winsock program
#include <stdio.h>       // for print functions
#include <stdlib.h>      // for exit() 
#include <winsock2.h>	 // for Winsock2 functions
#include <ws2tcpip.h>    // adds support for getaddrinfo & getnameinfo for v4+6 name resolution
#include <Ws2ipdef.h>    // optional - needed for MS IP Helper

// #define ALL required constants HERE, not inline 
// #define is a macro, don't terminate with ';'  For example...
#define RCVBUFSIZ 50

// declare any functions located in other .c files here
// I set it to be an external since you gave us the function in another file
extern void DisplayFatalErr(char* errMsg); // writes error message before abnormal termination

void main(int argc, char* argv[])   // argc is # of strings following command, argv[] is array of ptrs to the strings
{
	// Declare ALL variables and structures for main() HERE, NOT INLINE (including the following...)
	WSADATA wsaData;                // contains details about WinSock DLL implementation
	struct sockaddr_in6 serverInfo;	// standard IPv6 structure that holds server socket info
	SOCKET sock; // will hold the socket descriptor returned by socket(), declared as SOCKET to match byte length.
	int serverPort;
	size_t msgLen;
	char rcvBuffer[RCVBUFSIZ];
	int bytesRead, totalBytesRead = 0;

	// Verify correct number of command line arguments, else do the following:
	// fprintf(stderr, "Helpful error message goes here"\n");
	// exit(1);	  // ...and terminate with abnormal termination code (1)
	if (argc != 4) {
		fprintf(stderr, "Arg err. Usage: WSEchoClientv6 <server IPv6 address> <server port> <\"message to echo\">\n");
		exit(1);
	}

	// Retrieve the command line arguments. (Sanity checks not required, but port and IP addr will need
	// to be converted from char to network standard.  See slides 11-15 & 12-3 for details.)
	char* serverIP = argv[1];
	serverPort = atoi(argv[2]); // convert int port to network's order*
	char* message = argv[3];

	// Initialize Winsock 2.0 DLL. Returns 0 if ok. If this fails, fprint error message to stderr as above & exit(1).  
	if (WSAStartup(MAKEWORD(2, 0), &wsaData) != 0) {
		DisplayFatalErr("WSAStartup() failed.");
	}
	// Create an IPv6 TCP stream socket.  Now that Winsock DLL is loaded, we can signal any errors as shown on next line:
	// DisplayFatalErr("socket() function failed.");
	// DisplayFatalErr("socket() function failed.");
	// Display helpful confirmation messages after key socket calls like this:
	// printf("Socket created successfully.  Press any key to continue...");
	// getchar();     // needed to hold console screen open
	sock = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
	if (sock == INVALID_SOCKET) {
		DisplayFatalErr("socket() function failed.");
	}
	printf("Socket created successfully. Press enter to continue...\n");
	getchar();

	// If doing extra credit IPv4 address handling option, add the setsockopt() call as follows...
	// if (perrno = setsockopt(sock, IPROTO_IPV6, IPV6_V6ONLY, (char *)&v6Only, sizeof(v6Only)) != 0)
	//     DisplayFatalErr("setsockopt() function failed.");  

	// Zero out the sockaddr_in6 structure and load server info into it.  See slide 11-15.
	// Don't forget any necessary format conversions.
	memset(&serverInfo, 0, sizeof(serverInfo)); // zero out the structure
	serverInfo.sin6_family = AF_INET6; // address type = IPv6
	serverInfo.sin6_port = htons(serverPort); // convert int port to ntwk order*

	if (inet_pton(AF_INET6, serverIP, &serverInfo.sin6_addr) != 1) {
		DisplayFatalErr("inet_pton() failed to convert address.");
	}

	// Attempt connection to the server.  If it fails, call DisplayFatalErr() with appropriate message,
	// otherwise printf() confirmation message
	if (connect(sock, (struct sockaddr*)&serverInfo, sizeof(serverInfo)) == SOCKET_ERROR) {
		DisplayFatalErr("connect() function failed.");
	}
	printf("Connected to server successfully. Press enter to continue...\n");
	getchar();

	// Send message to server (without '\0' null terminator). Check for null msg (length=0) & verify all bytes were sent...
	// ...else call DisplayFatalErr() with appropriate message as before
	msgLen = strlen(message);
	if (msgLen == 0) {
		DisplayFatalErr("No message to send.");
	}

	int bytesSent = send(sock, message, msgLen, 0);
	if (bytesSent != msgLen) {
		DisplayFatalErr("send() function failed.");
	}
	printf("Message sent to server successfully. Bytes sent: %d\n", bytesSent);

	// Retrieve the message returned by server.  Be sure you've read the whole thing (could be multiple segments). 
	// Manage receive buffer to prevent overflow with a big message.
	// Call DisplayFatalErr() if this fails.  (Lots can go wrong here, see slides.)
	while (1) {
		bytesRead = recv(sock, rcvBuffer, RCVBUFSIZ - 1, 0);

		// Check if the connection has been closed by the server
		if (bytesRead == 0) {
			printf("Server closed the connection.\n");
			break;
		}

		// Check if recv() failed
		if (bytesRead == SOCKET_ERROR) {
			DisplayFatalErr("recv() failed.");
		}

		// Null-terminate and print the received data
		rcvBuffer[bytesRead] = '\0';
		printf("Received %d bytes: %s\n", bytesRead, rcvBuffer);
		totalBytesRead += bytesRead;

		if (totalBytesRead >= bytesSent) {
			printf("Received all expected data from server.\n");
			break;
		}
	}
	printf("\nReceived %d bytes from server.\n", totalBytesRead);

	// Close the TCP connection (send a FIN) & print appropriate message.
	if (closesocket(sock) == 0) {
		printf("Connection closed gracefully.\n");
	}
	else {
		DisplayFatalErr("Failed to close the connection.");
	}

	// Release the Winsock DLL
	WSACleanup();

	exit(0);
}
