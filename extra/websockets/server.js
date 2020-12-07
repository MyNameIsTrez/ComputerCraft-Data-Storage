// const express = require('express');
// const path = require('path');
const WebSocket = require('ws');
// const app = express();

const socketServer = new WebSocket.Server({port: 3030});

socketServer.on('connection', (socketClient) => {
	console.log('created connection');
	console.log('connected clients: ', socketServer.clients.size);

    socketClient.on('close', (socketClient) => {
        console.log('closed connection');
        console.log('connected clients: ', socketServer.clients.size);
    });
});