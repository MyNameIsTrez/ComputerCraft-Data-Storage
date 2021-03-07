// TODO: In C, these globals should be moved to main() and passed by address.

// NOT USER SETTINGS //

let w, h, r;
let gridSize, rSq;

let leftOpenArr, rightOpenArr;

let testNumber = 0;
let allTestsPassed = true;

let openCount;

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


function initOpenArr() {
	leftOpenArr = [];
	rightOpenArr = [];

	leftOpenArr[0] = 0;
	rightOpenArr[0] = gridSize - 1;

	openCount = gridSize;
}


function getRandomOpenIndex() {
	let nthOpenIndex = getRandomInt(openCount) + 1;

	let openIndexesSeen = 0;
	let difference, startOfLeft, offset;

	for (let index = 0; index < leftOpenArr.length; index++) {
		difference = rightOpenArr[index] - leftOpenArr[index] + 1;
		if (openIndexesSeen + difference >= nthOpenIndex) {
			startOfLeft = leftOpenArr[index] - 1;
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

	let newLeftOpenArr = [];
	let newRightOpenArr = [];

	const mx = index % w;
	const my = Math.floor(index / w);

	let yOffsetSq;

	const yOffsetMaxSq = Math.min(my, r) ** 2;
	const firstY = Math.max(0, my - r);

	if (getFirstIClosedLeft(rSq, yOffsetMaxSq, mx, firstY, w) != 0) {
		newLeftOpenArr.push(0);
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
			newRightOpenArr.push(iOpenRight);
		}

		iOpenLeft = iClosedRight + 1;
		if (iOpenLeft <= gridSize - 1) {
			newLeftOpenArr.push(iOpenLeft);
		}
	}

	if (getLastIClosedRight(rSq, yOffsetMaxSq, mx, firstY, w) != gridSize - 1) {
		newRightOpenArr.push(gridSize - 1);
	}

	combineOpenArrs(newLeftOpenArr, newRightOpenArr, w, h, gridSize);
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
 * Combines the ranges of open arrays.
 * It does this by doing an AND operation on the ranges.
 * [5, 7] means index 5, 6 and 7 are open.
 *
 * [     [1,15]     ] + [ [5,6], [9,10] ] = [ [5,6], [9,10] ]
 * [ [5, 6], [9,10] ] + [ [2,3], [6, 7] ] = [     [6,6]     ]
 */
function combineOpenArrs(newLeftOpenArr, newRightOpenArr, w, h, gridSize) {
	let oldLeftOpenArr = [...leftOpenArr];
	let oldRightOpenArr = [...rightOpenArr];

	const oldOpenArrLength = oldLeftOpenArr.length;
	const newOpenArrLength = newLeftOpenArr.length;

	let oldIndexLeft, oldIndexRight;

	let oldLeft, oldRight;
	let newLeft, newRight;

	let newLeftNext;

	let start, end;

	let combinedLeftOpenArr = []; // TODO: This array can be recycled in C.
	let combinedRightOpenArr = [];

	openCount = 0;

	// for (let newIndex = 0; newIndex < newOpenArrLength; newIndex++) {
	// 	newLeft = newLeftOpenArr[newIndex];
	// 	newRight = newRightOpenArr[newIndex];

	// 	oldIndexLeft = binarySearchClosestLeftIndex(newLeft, oldLeftOpenArr);
	// 	oldLeft = oldLeftOpenArr[oldIndexLeft];

	// 	oldIndexRight = binarySearchClosestRightIndex(newRight, oldRightOpenArr);
	// 	oldRight = oldRightOpenArr[oldIndexRight];


	// }





	for (let newIndex = 0; newIndex < newOpenArrLength; newIndex++) {
	    // console.log(newIndex, oldLeftOpenArr, oldRightOpenArr, newLeftOpenArr, newRightOpenArr)

		oldIndexLeft = binarySearchClosestLeftIndex(newLeftOpenArr[newIndex], oldLeftOpenArr);

		if (oldIndexLeft == -1) { // Should never be reached!
	        console.log("oldIndexLeft == -1!!");
	        continue;
	    }

		newLeft = newLeftOpenArr[newIndex];
		newRight = newRightOpenArr[newIndex];

		newLeftNext = newLeftOpenArr[newIndex + 1];

	    // console.log(newLeftNext); // TODO: Prints undefined!!

	    // TODO: Check if this is still repeated thousands of times per loop.
		while (oldIndexLeft < oldOpenArrLength) {
			oldLeft = oldLeftOpenArr[oldIndexLeft];
			start = Math.max(oldLeft, newLeft);
			
			oldRight = oldRightOpenArr[oldIndexLeft];
			end = Math.min(oldRight, newRight);

			if (end >= start) {
				combinedLeftOpenArr.push(start);
				combinedRightOpenArr.push(end);

				openCount += end - start + 1;
			}

			// if (newIndex + 1 <= newOpenArrLength && newLeftNext <= oldRight) {
			if (newIndex + 1 < newOpenArrLength && newLeftNext <= oldRight) {
				// newIndex++;
				break;
			} else {
				oldIndexLeft++;
			}
		}
	}

	leftOpenArr = [...combinedLeftOpenArr];
	rightOpenArr = [...combinedRightOpenArr];
}


function binarySearchClosestLeftIndex(searched, arr) {
	// TODO: In C this function could just use ints here instead of lets so the Math.floor below can be removed.
	let low = 0;
	let high = arr.length - 1;
	let mid;

	while (low <= high) {
		mid = Math.floor((high + low) / 2);
		// console.log(`low: ${low}, mid: ${mid}, high: ${high}, searched: ${searched}, arr[mid]: ${arr[mid]}, searched < arr[mid]: ${searched < arr[mid]}`);

		if (searched < arr[mid]) {
			high = mid - 1;
		} else if (searched > arr[mid]) {
			low = mid + 1;
		} else {
			// console.log("return 1");
			return mid;
		}
	}
	// console.log("return 2");
	// console.log(`low: ${low}, high: ${high}`);
	return Math.max(0, high); // This probably won't work in all cases.
	// return (arr[low] - searched) < (searched - arr[high]) ? low : high;
}


// function binarySearchClosestLeftIndex(searched, arr) {
// 	if (searched < arr[0]) {
// 	  return arr[0];
// 	}
// 	if (searched > arr[arr.length - 1]) {
// 	  return arr[arr.length - 1];
// 	}

// 	// TODO: In C this function could just use ints here instead of lets so the Math.floor() below can be removed.
// 	let low = 0;
// 	let high = arr.length - 1;
// 	let mid;

// 	// console.log("foo")
// 	while (low <= high) {
// 		mid = Math.floor((high + low) / 2);
// 		// console.log(`low: ${low}, mid: ${mid}, high: ${high}, searched: ${searched}, arr[mid]: ${arr[mid]}, searched < arr[mid]: ${searched < arr[mid]}, searched > arr[mid]: ${searched > arr[mid]}, arr: ${arr}`);

// 		if (searched < arr[mid]) {
// 			high = mid - 1;
// 		} else if (searched > arr[mid]) {
// 			low = mid + 1;
// 		} else {
// 			// console.log("bar")
// 			return mid;
// 		}
// 	}

// 	// console.log("baz");
// 	// console.log((arr[low] - searched) < (searched - arr[high]) ? low : high);
// 	return (arr[low] - searched) < (searched - arr[high]) ? low : high;
// }

// function binarySearchClosestRight(searched, arr) {
// 	if (searched < arr[0]) {
// 		return arr[0];
// 	}
// 	if (searched > arr[arr.length - 1]) {
// 		return arr[arr.length - 1];
// 	}
  
// 	// TODO: In C this function could just use ints here instead of lets so the Math.floor() below can be removed.
// 	let low = 0;
// 	let high = arr.length - 1;
// 	let mid;
  
// 	while (low <= high) {
// 		mid = Math.floor((high + low) / 2);
// 		// console.log(`low: ${low}, mid: ${mid}, high: ${high}, searched: ${searched}, arr[mid]: ${arr[mid]}, searched < arr[mid]: ${searched < arr[mid]}, searched > arr[mid]: ${searched > arr[mid]}, arr: ${arr}`);
	
// 		if (searched < arr[mid]) {
// 			high = mid - 1;
// 		} else if (searched > arr[mid]) {
// 			low = mid + 1;
// 		} else {
// 			return arr[mid];
// 		}
// 	}
  
// 	return (arr[low] - searched) < (searched - arr[high]) ? arr[high] : arr[low];
// }


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
	
	w = 512; // Width of grid.
	h = 512; // Height of grid.
	r = 1; // Radius of circle, 0 means a single 1x1 cell.

	gridSize = w * h;
	rSq = r ** 2;
	
	cellWidth = width / w;
	cellHeight = height / h;

	///////////////////

	initOpenArr();
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
			if (leftOpenArr.length != 0) {
				index = getRandomOpenIndex();
				placeCircle(index, r, w, h, gridSize, rSq);
				placed++;
			}
		}
	}
	
	if (frameCount % 60 == 0) {
		const open = leftOpenArr.length;
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