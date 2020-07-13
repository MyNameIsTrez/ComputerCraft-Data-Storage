const { spawn } = require("child_process");

const temperatures = []; // Store readings

const args = ["sensor.py"];
args.push(1)

const sensor = spawn("python", args);

// Gets called whenever print is called in Python
sensor.stdout.on("data", function (data) {
	// Converts Buffer object to Float
	temperatures.push(parseFloat(data));
	console.log(temperatures);
});