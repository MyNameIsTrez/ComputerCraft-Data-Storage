const fs = require("fs");
const express = require("express");
const bodyParser = require("body-parser");
const Datastore = require("nedb");
const { spawn } = require("child_process");

const app = express();
// TODO: Might want to remove "0.0.0.0", because I don't know if it does anything atm,
// and because it might be a security risk.
app.listen(3000, "0.0.0.0", () => {
	console.log("Listening at port 3000");
});

// ComputerCraft versions below 1.63 don't support custom headers,
// so the content-type of those is always 'application/x-www-form-urlencoded'.
app.use(bodyParser.urlencoded({ extended: true }));

const sleep = ms => {
	return new Promise(resolve => setTimeout(resolve, ms));
}

const dbInsert = entry => {
	// return sleep(1000).then(_ => 69);
	return new Promise(function (resolve, reject) {
		db.insert(entry, (err, inserted) => {
			if (err) reject(err);
			else resolve(inserted._id);
		});
	});
}


const foo = async info => {
	console.log('Start');

	const promises = info.entries.map(async entry => {
		const id = await dbInsert(entry);
		return id;
	})

	const entryIDs = await Promise.all(promises);
	console.log(`entryIDs: ${entryIDs}`);

	console.log('End');

	// renderAscii(info.entries, entryIDs);

	// let entryIDs = {};
	// for (const entry of info.entries) {
	// 	dbInsertEntry(entry)
	// 		.then(cake => console.log(cake))
	// 		.catch(err => console.log(err))
	// 	// const id = dbInsertEntry(entry, entryIDs, (id, entryIDs) => {
	// 	// 	entryIDs.push(id);
	// 	// 	createAsciiFolder(id);
	// 	// 	console.log(`1: ${entryIDs}`);
	// 	// });
	// 	// console.log(`2: ${entryIDs}`);
	// }
}

app.post("/add", (request, response) => {
	const info = repairMangledInfo(request.body);
	const format = checkInfoFormat(info);
	if (format === true) {
		foo(info);
	} else {
		createError(format);
	}
	// ComputerCraft v1.33 doesn't feature http.post returning anything,
	// so don't bother sending anything back.
	response.end();
});

function repairMangledInfo(mangledInfo) {
	const key = getMangledKey(mangledInfo);
	const value = mangledInfo[key]
	return JSON.parse(value);
}

function getMangledKey(mangledObj) {
	return Object.keys(mangledObj)[0];
}

function checkInfoFormat(info) {
	if (info.password != "MyNameIsTrez") {
		return "Wrong password";
	}
	// TODO: Check if the incoming info is in the correct format.
	// 1. The correct password was used, 2. All fields filled with the correct types and 3. All URLs exist.
	return true;
}

const db = new Datastore({
	filename: "ascii-info.db", autoload: true
});

function createAsciiFolder(id) {
	fs.mkdirSync(`ascii-frames/${id}`);
}

const dbInsertEntry = entry => {
	return new Promise((resolve, reject) => {
		db.insert(entry, (err, inserted) => {
			if (err) reject(err);
			resolve(inserted._id);
		});
	})
}

// function dbInsertEntry(entry) {
// 	db.insert(entry, (err, inserted) => {
// 		if (err) throw err;
// 		return inserted._id;
// 	});
// }

function renderAscii(entry, entryIDs) {
	// const args = [JSON.stringify(entry), JSON.stringify(entryIDs)];
	// console.log(args);
	// const sensor = spawn("python", ["python/render.py"].concat(args));

	// // Prints whatever Python has attempted to print
	// sensor.stdout.on("data", function (buffer) {
	// 	console.log(buffer.toString());
	// });
}

function createError(err) {
	// TODO: It'd be nice if ComputerCraft would send a GET right after POSTing the info, to an 'error' server page,
	// for the purpose of seeing what the reason was that this function has rejected its sent info.
	console.log(err);
}