const fs = require("fs");
const express = require("express");
const bodyParser = require("body-parser");
const Datastore = require("nedb");

const app = express();
// Might want to remove "0.0.0.0", because I don't know if it does anything atm,
// and because it might be a security risk.
app.listen(3000, "0.0.0.0", () => {
	console.log("Listening at port 3000");
});

// ComputerCraft versions below 1.63 don't support custom headers,
// so the content-type of those is always 'application/x-www-form-urlencoded'
app.use(bodyParser.urlencoded({ extended: true }));

app.post("/add", (request, response) => {
	const info = repairMangledInfo(request.body);
	if (checkInfoFormat(info)) {

	}
	// ComputerCraft v1.33 doesn't feature http.post returning anything,
	// so don't bother sending anything back
	response.end();
});

function repairMangledInfo(mangledInfo) {
	const key1 = getMangledKey(mangledInfo);
	const value = mangledInfo[key1];
	const key2 = getMangledKey(value);
	return JSON.parse(key1 + "[" + key2 + "]}]}");
}

function getMangledKey(mangledObj) {
	return Object.keys(mangledObj)[0];
}

function checkInfoFormat(info) {
	// TODO: Check if the incoming info is in the correct format.
	// 1. All fields filled with the correct types and 2. URL(s) exist.
	// It'd be nice if ComputerCraft would send a GET right after POSTing the info, to an 'error' server page,
	// for the purpose of seeing what the reason was that this function has rejected its sent info.
	console.log("info:");
	console.log(info);
}

const db = new Datastore({
	filename: "ascii-info.db", autoload: true
});

// processPOST(JSON.parse(fs.readFileSync("input.txt", "utf8")));

function processPOST(info) {
	dbInsertInfo(info, (id) => {
		createAsciiFolder(id);
		renderAsciiPython(info, id);
	});
}

function createAsciiFolder(id) {
	fs.mkdirSync(`ascii-frames/${id}`);
}

function dbInsertInfo(info, callback) {
	db.insert(info, (err, inserted) => {
		if (err) throw err;
		callback(inserted._id);
	});
}

function renderAsciiPython() {
	// Add code that calls Python ascii rendering function here
}