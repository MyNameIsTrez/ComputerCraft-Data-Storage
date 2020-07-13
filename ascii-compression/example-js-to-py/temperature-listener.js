const { spawn } = require("child_process");

const temperatures = []; // Store readings

const args = ["sensor.py"];
args.push(1)

const sensor = spawn("python", args);

// Gets whatever Python has printed
sensor.stdout.on("data", function (data) {
	// Converts Buffer object to Float
	temperatures.push(parseFloat(data));
	console.log(temperatures);
});