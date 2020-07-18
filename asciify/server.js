const fs = require("fs")
const express = require("express")
const bodyParser = require("body-parser")
const Datastore = require("nedb")
const { spawn } = require("child_process")

const app = express()
// TODO: Might want to remove "0.0.0.0", because I don't know if it does anything atm,
// and because it might be a security risk.
app.listen(3000, "0.0.0.0", () => {
	console.log("Listening at port 3000")
})

// ComputerCraft versions below 1.63 don't support custom headers,
// so the content-type of those is always 'application/x-www-form-urlencoded'.
app.use(bodyParser.urlencoded({ extended: true }))

const db = new Datastore({
	filename: "ascii-info.db", autoload: true
})

app.post("/ascii-add", async (req, res) => {
	const info = repairMangledInfo(req.body)
	const format = checkInfoFormat(info)
	if (format === true) {
		const entriesWithVariationIDs = await dbAddVariations(info.entries)
		renderAscii(entriesWithVariationIDs)
	} else {
		createError(format)
	}
	// ComputerCraft v1.33 doesn't feature http.post returning anything, so don't bother replying back.
	res.end()
})

function repairMangledInfo(mangledInfo) {
	const key = getMangledKey(mangledInfo)
	const value = mangledInfo[key]
	return JSON.parse(value)
}

function getMangledKey(mangledObj) {
	return Object.keys(mangledObj)[0]
}

function checkInfoFormat(info) {
	if (info.password != "MyNameIsTrez") {
		return "Wrong password"
	}
	// TODO: Check if the incoming info is in the correct format.
	// 1. The correct password was used, 2. All fields filled with the correct types and 3. All URLs exist.
	return true
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
			}
			variation.id = await dbInsertVariation(variationInfo)
		}
	}
	return entries // TODO: Can this line be removed?
}

async function dbInsertVariation(variation) {
	return new Promise(function (resolve, reject) {
		db.insert(variation, (err, inserted) => {
			if (err) reject(err)
			else resolve(inserted._id)
		})
	})
}

function renderAscii(entries) {
	// console.log(JSON.stringify(entries, undefined, 2))
	const py = spawn("python", ["python/render.py"])

	// Prints whatever Python has attempted to print
	py.stderr.on("data", (data) => {
		console.error(`stderr: ${data}`)
	})

	py.stdout.on("data", (buffer) => {
		const input = buffer.toString()
		// Important objects are sent through python's print(), other information is written to output.txt.
		try {
			dbAppendInfo(JSON.parse(input))
		} catch (err) {
			console.log(err)
			console.log(input)
		}
	})

	py.stdin.write(JSON.stringify(entries))
	py.stdin.end() // TODO: Necessary?
}

function dbAppendInfo(extraVariationsInfo) {
	for (const [id, info] of Object.entries(extraVariationsInfo)) {
		db.update({ _id: id }, {
			$set: { "frame_files_count": info.frame_files_count, "frame_count": info.frame_count }
		}, {}, function () { })
	}
}

function createError(err) {
	// TODO: It'd be nice if ComputerCraft would send a GET right after POSTing the info, to an '/error' server endpoint,
	// for the purpose of seeing what the reason was that this function has rejected its sent info.
	console.log(err)
}

app.get("/ascii-info", async (req, res) => { db.find({}, function (err, docs) { res.send(docs) }) })

app.get("/ascii-output", (req, res) => res.download("output.txt"))

app.post("/ascii-file", (req, res) => {
	const fileID = repairMangledInfo(req.body)
	const path = `ascii-frames/ktFgVkXKqm21IF1f/${fileID}.txt`
	fs.access(path, fs.F_OK, (err) => {
		if (err) {
			// File doesn't exist.
			res.send("error")
			return
		}
		// File exists.
		res.download(path)
	})
})