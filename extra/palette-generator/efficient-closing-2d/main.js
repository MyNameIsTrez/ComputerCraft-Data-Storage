// TODO: In C, these globals should be moved to main() and passed by address.

// NOT USER SETTINGS //

let w, h, r;
let gridSize, rSq;

let leftOpenIndexes, rightOpenIndexes;

let testNumber = 0;
let allTestsPassed = true;

let openIndexCount;

//// USED IN DRAWCIRCLES() ////

const framesBetweenPlacement = 1; // 1 is max speed.
const placeSpeedMultiplier = 100; // 10
const drawing = true;
const drawSquares = true; // If false it'll draw circles.
const printPlacementStats = true;

const colors = [
	[50, 50, 200],
	[50, 200, 50],
	[50, 200, 200],
	[200, 50, 50],
	[200, 50, 200],
	[200, 200, 50],
	[200, 200, 200],
];

let placed = 0;
let prevOpen = 0;
let prevPlacedPerSec = 0;
let prevTime = performance.now();

let colorIndex = 0;

let cellWidth, cellHeight;

////////////////////


function initOpenIndexes() {
	leftOpenIndexes = [];
	rightOpenIndexes = [];

	leftOpenIndexes[0] = 0;
	rightOpenIndexes[0] = gridSize - 1;

	openIndexCount = gridSize;
}


function getRandomOpenIndex() {
	let nthOpenIndex = getRandomInt(openIndexCount) + 1;

	let openIndexesSeen = 0;
	let difference, startOfLeft, offset;

	for (let index = 0; index < leftOpenIndexes.length; index++) {
		difference = rightOpenIndexes[index] - leftOpenIndexes[index] + 1;
		if (openIndexesSeen + difference >= nthOpenIndex) {
			startOfLeft = leftOpenIndexes[index] - 1;
			offset = nthOpenIndex - openIndexesSeen;
			return startOfLeft + offset;
		} else {
			openIndexesSeen += difference;
		}
	}
}


function getRandomInt(max) {
	return Math.floor(Math.random() * max);
}


function placeCircle(index, r, w, h, gridSize, rSq) {
	let xClosedLeft, xClosedRight;
	let iClosedLeft, iClosedRight;
	let iOpenLeft, iOpenRight;

	let newLeftOpenIndexes = [];
	let newRightOpenIndexes = [];

	const mx = index % w;
	const my = Math.floor(index / w);

	let yOffsetSq;

	const yOffsetMaxSq = Math.min(my, r) ** 2;
	const firstY = Math.max(0, my - r);

	if (getFirstIClosedLeft(rSq, yOffsetMaxSq, mx, firstY, w) != 0) {
		newLeftOpenIndexes.push(0);
	}

	for (let y = Math.max(0, my - r); y < Math.min(h, my + r + 1); y++) {
		yOffsetSq = (my - y) ** 2;

		xClosedLeft = getXClosedLeft(rSq, yOffsetSq, mx);
		xClosedRight = getXClosedRight(rSq, yOffsetSq, mx);

		if (drawing) {
			if (drawSquares) {
				drawRect(xClosedLeft, y, xClosedRight + 1, y + 1, w, h);
			} else {
				const mxScaled = mx * cellWidth;
				const myScaled = my * cellHeight;
				const rScaled = r * cellWidth;
				circle(mxScaled, myScaled, rScaled);
			}
		}

		iClosedLeft = xClosedLeft + y * w;
		iClosedRight = xClosedRight + y * w;

		iOpenRight = iClosedLeft - 1;
		if (iOpenRight >= 0) {
			newRightOpenIndexes.push(iOpenRight);
		}

		iOpenLeft = iClosedRight + 1;
		if (iOpenLeft <= gridSize - 1) {
			newLeftOpenIndexes.push(iOpenLeft);
		}
	}

	if (getLastIClosedRight(rSq, yOffsetMaxSq, mx, firstY, w) != gridSize - 1) {
		newRightOpenIndexes.push(gridSize - 1);
	}

	combineOpenIndexes(newLeftOpenIndexes, newRightOpenIndexes, w, h, gridSize);
}


function getFirstIClosedLeft(rSq, yOffsetMaxSq, mx, firstY, w) {
	const xClosedLeft = getXClosedLeft(rSq, yOffsetMaxSq, mx);
	return xToIndex(xClosedLeft, firstY, w);
}


function getLastIClosedRight(rSq, yOffsetMaxSq, mx, firstY, w) {
	const xClosedRight = getXClosedRight(rSq, yOffsetMaxSq, mx);
	return xToIndex(xClosedRight, firstY, w);
}


/*
 * Circle: (xOffset - mx)^2 + (yOffset - my)^2 = r^2
 * Unit circle: xOffset^2 + yOffset^2 = r^2
 * xOffset^2 = rSq - yOffsetSq
 * xOffset = ± sqrt(rSq - yOffsetSq)
 */
function getXClosedLeft(rSq, yOffsetSq, mx) {
	const xOffset = Math.sqrt(rSq - yOffsetSq);
	return Math.max(0, mx - xOffset);
}


function getXClosedRight(rSq, yOffsetSq, mx) {
	const xOffset = Math.sqrt(rSq - yOffsetSq);
	return Math.min(w - 1, mx + xOffset);
}


function xToIndex(x, y, w) {
	return x + y * w;
}


/*
 * Combines the ranges of open indexes.
 * It does this by doing an AND operation on the ranges.
 * [5, 7] means index 5, 6 and 7 are open.
 *
 * [     [1,15]     ] + [ [5,6], [9,10] ] = [ [5,6], [9,10] ]
 * [ [5, 6], [9,10] ] + [ [2,3], [6, 7] ] = [     [6,6]     ]
 */
function combineOpenIndexes(newLeftOpenIndexes, newRightOpenIndexes, w, h, gridSize) {
	let oldLeftOpenIndexes = [...leftOpenIndexes];
	let oldRightOpenIndexes = [...rightOpenIndexes];

	const oldOpenIndexesLength = oldLeftOpenIndexes.length;
	const newOpenIndexesLength = newLeftOpenIndexes.length;

	let oldIndex;

	let newLeftIndex, newRightIndex, newLeftIndexNext;

	let start, end;

	let combinedLeftOpenIndexes = []; // Max indexes can be calculated and used so this array can be recycled in C.
	let combinedRightOpenIndexes = [];

	openIndexCount = 0;

	// TODO: Look into ropes (binary tree structure) as faster algorithm.

	for (let newIndex = 0; newIndex < newOpenIndexesLength; newIndex++) {
		oldIndex = binarySearchClosest(newLeftOpenIndexes[newIndex], newRightOpenIndexes[newIndex], oldLeftOpenIndexes, oldRightOpenIndexes);

		// console.log(`newLeftOpenIndexes[newIndex]: ${newLeftOpenIndexes[newIndex]}, newRightOpenIndexes[newIndex]: ${newRightOpenIndexes[newIndex]}, oldLeftOpenIndexes: ${oldLeftOpenIndexes}, oldRightOpenIndexes: ${oldRightOpenIndexes}`);
		// console.log(`oldIndex: ${oldIndex}`);

		if (oldIndex == -1) continue; // Error handling may be unnecessary.

		newLeftIndex = newLeftOpenIndexes[newIndex];
		newRightIndex = newRightOpenIndexes[newIndex];

		newLeftIndexNext = newLeftOpenIndexes[newIndex + 1];

		while (oldIndex < oldOpenIndexesLength) {
			start = Math.max(oldLeftOpenIndexes[oldIndex], newLeftIndex);
			end = Math.min(oldRightOpenIndexes[oldIndex], newRightIndex);

			if (end >= start) {
				combinedLeftOpenIndexes.push(start);
				combinedRightOpenIndexes.push(end);

				openIndexCount += end - start + 1;
			}

			if (newIndex + 1 <= newOpenIndexesLength && newLeftIndexNext <= oldRightOpenIndexes[oldIndex]) {
				// newIndex++;
				break;
			} else {
				oldIndex++;
			}
		}
	}

	leftOpenIndexes = [...combinedLeftOpenIndexes];
	rightOpenIndexes = [...combinedRightOpenIndexes];

	// console.log(leftOpenIndexes, rightOpenIndexes);
	// console.log();
}


function binarySearchClosest(newLeft, newRight, oldLeftArr, oldRightArr) {
	const value = newLeft;

	if (newRight < oldLeftArr[0]) return -1; // -1 means that it should be skipped, might be an unnecessary check.
	if (newLeft > oldRightArr[oldRightArr.length - 1]) return -1;

	// TODO: In C this function could just use ints here instead of lets so the Math.floor below can be removed.
	let low = 0;
	let high = oldLeftArr.length - 1;
	let mid;

	while (low <= high) {
		mid = Math.floor((high + low) / 2);
		// console.log(`low: ${low}, mid: ${mid}, high: ${high}, value: ${value}, oldLeftArr[mid]: ${oldLeftArr[mid]}, value < oldLeftArr[mid]: ${value < oldLeftArr[mid]}`);

		if (value < oldLeftArr[mid]) {
			high = mid - 1;
		} else if (value > oldLeftArr[mid]) {
			low = mid + 1;
		} else {
			// console.log("return 1");
			return mid;
		}
	}
	// console.log("return 2");
	// console.log(`low: ${low}, high: ${high}`);
	return Math.max(0, high); // This probably won't work in all cases.
	// return (oldLeftArr[low] - value) < (value - oldLeftArr[high]) ? low : high;
}


function initDrawGrid() {
	const sideLength = Math.min(innerWidth - 1, innerHeight - 1);
	createCanvas(sideLength, sideLength);

	// rectMode(RADIUS);
	rectMode(CORNERS);
	textAlign(CENTER, CENTER);
	// ellipseMode(RADIUS);

	noSmooth();

	stroke(175, 50, 50);
	fill(175, 50, 50);
}


function drawRect(x1, y1, x2, y2, w, h) {
	const widthMult = cellWidth;
	const heightMult = cellHeight;
	
	const x1_ = x1 * widthMult;
	const y1_ = y1 * heightMult;
	const x2_ = x2 * widthMult;
	const y2_ = y2 * heightMult;
	rect(x1_, y1_, x2_, y2_);
}


function setup() {
	initDrawGrid();
	runTests();

	// USER SETTINGS //
	
	w = 256; // Width of grid.
	h = 256; // Height of grid.
	r = 1; // Radius of circle, 0 means a single 1x1 cell.

	gridSize = w * h;
	rSq = r ** 2;
	
	cellWidth = width / w;
	cellHeight = height / h;

	///////////////////

	initOpenIndexes();
}


function draw() {
	if (allTestsPassed) {
		drawCircles();
	}
}


function drawCircles() {		
	let chosenColor;
	let index;
	
	if (frameCount % framesBetweenPlacement == 0) {
		chosenColor = colors[colorIndex++ % colors.length];
		fill(chosenColor);
		stroke(chosenColor);
	
		for (let i = 0; i < placeSpeedMultiplier; i++) {
			if (leftOpenIndexes.length != 0) {
				index = getRandomOpenIndex();
				placeCircle(index, r, w, h, gridSize, rSq);
				placed++;
			}
		}
	}
	
	if (frameCount % 60 == 0) {
		const open = leftOpenIndexes.length;
		const placedPerSec = Math.floor(placed / ((performance.now() - prevTime) / 1000));
		
		if (printPlacementStats) {
			console.log(`open: ${open} (${open-prevOpen}), placed/second: ${placedPerSec} (${placedPerSec-prevPlacedPerSec})`);
		}

		prevOpen = open;
		prevPlacedPerSec = placedPerSec;
		placed = 0;
		prevTime = performance.now();
	}
}