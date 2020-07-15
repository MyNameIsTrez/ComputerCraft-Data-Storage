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

async function dbInsertVariation(variation) {
	return new Promise(function (resolve, reject) {
		db.insert(variation, (err, inserted) => {
			if (err) reject(err);
			else resolve(inserted._id);
		});
	});
}

async function dbAddVariations(entries) {
	for (const entry of entries) {
		for (const variation of entry.variations) {
			const variationInfo = {
				"url": entry.url,
				"url_name": entry.url_name,
				"extension": entry.extension,
				"displayed_name": variation.displayed_name,
				"palette": variation.palette,
				"width": variation.width,
				"height": variation.height,
			};
			variation.id = await dbInsertVariation(variationInfo);
		}
	}
	return entries; // TODO: Can this line be removed?
}

app.post("/add", async (request, response) => {
	const info = repairMangledInfo(request.body);
	const format = checkInfoFormat(info);
	if (format === true) {
		const entriesWithVariationIDs = await dbAddVariations(info.entries);
		renderAscii(entriesWithVariationIDs);
	} else {
		createError(format);
	}
	// ComputerCraft v1.33 doesn't feature http.post returning anything, so don't bother replying back.
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

function renderAscii(entries) {
	// console.log(JSON.stringify(entries, undefined, 2));
	const py = spawn("python", ["python/render.py"]);
	// Prints whatever Python has attempted to print
	py.stderr.on("data", (data) => {
		console.error(`stderr: ${data}`);
	});
	py.stdout.on("data", (buffer) => {
		const str = buffer.toString();
		// Additional info is detected by being JSON.
		// It would be better to send it on a separate channel instead.
		try {
			// Keys of objects get printed with ' instead of ", which JSON.parse doesn't like.
			const obj = JSON.parse(str.replace(/'/g, '"'));
			console.log(`\nDone! Duration: ${obj.duration.minutes} minutes, ${obj.duration.seconds} seconds.`);
			// console.log(obj.additional_variations_info);
			// dbAppendInfo(additionalVariationsInfo);
		} catch (error) {
			console.log(str);
		}
	});
	py.stdin.write(JSON.stringify(entries));
	py.stdin.end();
}

function createError(err) {
	// TODO: It'd be nice if ComputerCraft would send a GET right after POSTing the info, to an 'error' server page,
	// for the purpose of seeing what the reason was that this function has rejected its sent info.
	console.log(err);
}