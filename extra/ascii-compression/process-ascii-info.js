const express = require("express");
const Datastore = require("nedb");

const app = express();
app.listen(3000, "0.0.0.0", () => {
	console.log("Listening at port 3000");
});
app.use(express.static("public"));
app.use(express.json());

app.post("/add", (request, response) => {
	console.log(request.body);
	// console.log(request);
});

const db = new Datastore({
	filename: "ascii-info.db", autoload: true
});

processPOST(JSON.parse(fs.readFileSync("input.txt", "utf8")));

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