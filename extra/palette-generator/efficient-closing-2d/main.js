// TODO: In C, these globals should be moved to main() and passed by address.

// NOT USER SETTINGS //

let w, h, r;
let gridSize, maxDistSq;

let leftOpenIndexes, rightOpenIndexes;

let testNumber = 0;
let allTestsPassed = true;

//// USED IN DRAWCIRCLES() ////

const framesBetweenPlacement = 1; // 1 is max speed.
const placeSpeedMultiplier = 10; // 10
const drawing = true;
const drawSquares = true; // If false it'll draw circles.
const printPlacementStats = false;

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

////////////////////


function initOpenIndexes() {
    leftOpenIndexes = [];
    rightOpenIndexes = [];

    leftOpenIndexes[0] = 0;
    rightOpenIndexes[0] = gridSize - 1;
}


function getRandomOpenIndex() {
    let nthOpenIndex = getRandomInt(getOpenIndexCount()) + 1;

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


 // TODO: Replace with code that continuously decrements openIndexCount instead for better time complexity.
function getOpenIndexCount() {
  let openIndexCount = 0;

  for (let index = 0; index < leftOpenIndexes.length; index++) {
    openIndexCount += rightOpenIndexes[index] - leftOpenIndexes[index] + 1;
  }

  return openIndexCount;
}


function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}


function placeCircle(index, r, w, h, gridSize, maxDistSq) {
  let xClosedLeft, xClosedRight;
  let iClosedLeft, iClosedRight;
  let iOpenLeft, iOpenRight;

  let newLeftOpenIndexes = [];
  let newRightOpenIndexes = [];

  const mx = index % w;
  const my = Math.floor(index / w);

  let yDiffSq;

  if (getFirstIClosedLeft(my, r, h, mx, maxDistSq, w) != 0) {
    newLeftOpenIndexes.push(0);
  }

  for (let y = Math.max(0, my - r); y < Math.min(h, my + r + 1); y++) {
    yDiffSq = (my - y) ** 2;

    xClosedLeft = getXClosedLeft(mx, r, yDiffSq, maxDistSq);
    xClosedRight = getXClosedRight(h, mx, r, yDiffSq, maxDistSq);

    if (drawing) {
        if (drawSquares) {
            drawRect(xClosedLeft, y, xClosedRight + 1, y + 1, w, h);
        } else {
            const mxScaled = mx * (width / w);
            const myScaled = my * (height / h);
            const rScaled = r * width / w;
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

  if (getLastIClosedRight(my, r, h, mx, maxDistSq, w) != gridSize - 1) {
    newRightOpenIndexes.push(gridSize - 1);
  }

  combineOpenIndexes(newLeftOpenIndexes, newRightOpenIndexes, w, h, gridSize);
}


function getFirstIClosedLeft(my, r, h, mx, maxDistSq, w) {
  if (Math.max(0, my - r) < Math.min(h, my + r + 1)) {
    const firstY = Math.max(0, my - r);
    const yDiffSq = (my - firstY) ** 2;
    const xClosedLeft = getXClosedLeft(mx, r, yDiffSq, maxDistSq);
    const iClosedLeft = xToIndex(xClosedLeft, firstY, w);
    console.log(iClosedLeft);
    // console.log(y, yDiffSq, xClosedLeft, iClosedLeft);
    return iClosedLeft;
  }
}


function getLastIClosedRight(my, r, h, mx, maxDistSq, w) {
  if (Math.max(0, my - r) < Math.min(h, my + r + 1)) {
    const lastY = Math.min(h, my + r + 1) - 1;
    const yDiffSq = (my - lastY) ** 2;
    const xClosedRight = getXClosedRight(h, mx, r, yDiffSq, maxDistSq);
    const iClosedRight = xToIndex(xClosedRight, lastY, w);
    return iClosedRight;
  }
}


function xToIndex(x, y, w) {
  return x + y * w;
}


function getXClosedLeft(mx, r, yDiffSq, maxDistSq) {
  let xLeft, distLeftSq;

  xLeft = Math.max(0, mx - r);

  // (x - mx)^2 + (y - my)^2 = r^2
  // 
  distLeftSq = (mx - xLeft) ** 2 + yDiffSq;

  while (distLeftSq > maxDistSq) { // TODO: May loop infinitely due to my - y?
    xLeft++;
    distLeftSq = (mx - xLeft) ** 2 + yDiffSq;
  }

  return xLeft;
}


function getXClosedRight(h, mx, r, yDiffSq, maxDistSq) {
  let xRight, distRightSq;

  xRight = Math.min(h - 1, mx + r);

  distRightSq = (xRight - mx) ** 2 + yDiffSq;

  while (distRightSq > maxDistSq) {
    xRight--;
    distRightSq = (xRight - mx) ** 2 + yDiffSq;
  }

  return xRight;
}


/*
 ** Combines the ranges of open indexes.
 ** It does this by doing an AND operation on the ranges.
 ** [5, 7] means index 5, 6 and 7 are open.
 **
 ** [     [1,15]     ] + [ [5,6], [9,10] ] = [ [5,6], [9,10] ]
 ** [ [5, 6], [9,10] ] + [ [2,3], [6, 7] ] = [     [6,6]     ]
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

  let closestIndex;

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
    const widthMult = width / w;
    const heightMult = height / h;
    
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
    maxDistSq = r ** 2;

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
                placeCircle(index, r, w, h, gridSize, maxDistSq);
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