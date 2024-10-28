// CS 2690 Program 2
// Simple Windows Sockets Echo Server (IPv6)
// Last update: 10/26/2024
// Rylan Cunningham 601 10/26/2024
// Windows 11 VS Community 2022
//
// Usage: WSEchoServerv6 <server port>
// Companion server is WSEchoServerv6
// Client Usage: WSEchoServerv6 <server IPv6 address> <server port> <"message to echo">
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
#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <Ws2ipdef.h>

#define DEFAULT_PORT 5000
#define MAXQUEUED 5

// External function declarations
// Writes error message before abnormal termination
extern void DisplayFatalErr(char* errMsg);
extern void ProcessClient(SOCKET clientSock);

int main(int argc, char* aqrgv[]) {
	WSADATA wsaData;
	SOCKET serverSock;
	struct sockaddr_in6 serverInfo;
	unsigned short serverPort = DEFAULT_PORT;

	// Initialize the WinSock DLL for version 2.0
	if (WSAStartup(MAKEWORD(2, 0), &wsaData) != 0) {
		DisplayFatalErr("WSAStartup() failed.");
		exit(1);
	}

	// Create a TCP socket using IPv6
	serverSock = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
	if (serverSock == INVALID_SOCKET) {
		DisplayFatalErr("socket() failed to create socket.");
	}

	// Get the server port number from the command line or use default port
	if (argc == 2) {
		serverPort = (unsigned short)atoi(aqrgv[1]);
	}
	else {
		printf("No port provided, using the default port %d\n", DEFAULT_PORT);
	}

	// Initialize the server address sockaddr_in6 structure (set to zero)
	memset(&serverInfo, 0, sizeof(serverInfo));
	serverInfo.sin6_family = AF_INET6; // IPv6
	serverInfo.sin6_port = htons(serverPort); // Convert port to big endian
	serverInfo.sin6_addr = in6addr_any; // Listen on all interfaces	

	// Bind the server socket to the local address and port
	if (bind(serverSock, (struct sockaddr*)&serverInfo, sizeof(serverInfo)) == SOCKET_ERROR) {
		DisplayFatalErr("bind() failed to bind server socket.");
	}

	// Set the server socket to listen for incoming connections
	if (listen(serverSock, MAXQUEUED) == SOCKET_ERROR) {
		DisplayFatalErr("listen() failed to set server socket to listen.");
	}

	printf("RC's IPv6 echo server is ready for client connection on port %d...\n", serverPort);

	// Forever loop to accept incoming client connections 
	for (;;) {
		struct sockaddr_in6 clientInfo; // Client address information
		int clientInfoLen = sizeof(clientInfo);

		// Accept an incoming client connection request
		SOCKET clientSock = accept(serverSock, (struct sockaddr*)&clientInfo, &clientInfoLen);
		if (clientSock == INVALID_SOCKET) {
			DisplayFatalErr("accept() failed to accept client connection.");
		}

		// Convert the client's IP address from network format to a readable string
		char clientIP[INET6_ADDRSTRLEN];
		inet_ntop(AF_INET6, &clientInfo.sin6_addr, clientIP, sizeof(clientIP));
		int clientPort = ntohs(clientInfo.sin6_port);
		printf("Processing the client at %s, client port %d, server port %d\n", clientIP, clientPort, serverPort);

		// Process the client connection in ProcessClient()
		ProcessClient(clientSock);
	}
	return 0;
}
