// ProcessClient.c
// Handles communication with a client. This function is called by the server to 
// process the client's messages, echo them back, and then close the connection.

#include <stdio.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <Ws2ipdef.h>

#define RCVBUFSIZ 50 // receive buffer size set to 50 bytes

// External error display function
extern void DisplayFatalErr(char* errMsg);

// Function to process client messages
void ProcessClient(SOCKET clientSock) {
    char rcvBuffer[RCVBUFSIZ];  // Declare the receive buffer
    int bytesReceived;

    // Receive data from the client
    while ((bytesReceived = recv(clientSock, rcvBuffer, RCVBUFSIZ, 0)) > 0) {
        if (bytesReceived < RCVBUFSIZ) {
            rcvBuffer[bytesReceived] = '\0';
        }
        // Echo the message back to the client
        int bytesSent = send(clientSock, rcvBuffer, bytesReceived, 0);
        if (bytesSent == SOCKET_ERROR || bytesSent != bytesReceived) {
            DisplayFatalErr("send() failed while echoing message.");
        }
        printf("Received %d bytes: %s\n", bytesReceived, rcvBuffer);

        memset(rcvBuffer, 0, RCVBUFSIZ);  // Clear the buffer
    }

    // Check for errors in recv()
    if (bytesReceived == SOCKET_ERROR) {
        DisplayFatalErr("recv() failed while receiving client message.");
    } else if (bytesReceived == 0) {
        printf("Client disconnected.\n");
    }

    // Close the client socket after communication
    if (closesocket(clientSock) == 0) {
        printf("Client connection closed gracefully.\n");
    } else {
        DisplayFatalErr("Failed to close the client connection.");
    }
}
