const { spawn } = require("child_process");

var child = spawn('python', ['child.py'], {
	stdio: [null, null, null, 'ipc']
});

// console.log("child:");
// console.log(child);

child.on('message', function (message) {
	console.log('Received message...');
	console.log(message);
});