////////////////////
// TODO: In C these globals should be replaced and be passed by address.
let circlesPlaced = 0;

let leftOpenIndexes = [];
let rightOpenIndexes = [];

let placed = 0;
let prevTime = performance.now();

let drawing = true;
////////////////////


function initOpenIndexes(gridSize) {
  leftOpenIndexes[0] = 0;
  rightOpenIndexes[0] = gridSize - 1;
}


function getRandomOpenIndex() {
  let nthOpenIndex = getRandomInt(getOpenIndexCount()) + 1; // TODO: Starts from 1, but may need to start from 0.
  // console.log(`nthOpenIndex: ${nthOpenIndex}`);

  const leftOpenIndexesLength = leftOpenIndexes.length;

  let openIndexesSeen = 0;
  let difference, closedIndex, openIndexesToSee;

  for (let index = 0; index < leftOpenIndexesLength; index++) {
    difference = rightOpenIndexes[index] - leftOpenIndexes[index] + 1;
    // console.log(`difference: ${difference}`);
    // console.log(`openIndexesSeen + difference: ${openIndexesSeen + difference}`);

    if (openIndexesSeen + difference >= nthOpenIndex) {
      closedIndex = leftOpenIndexes[index] - 1;
      openIndexesToSee = nthOpenIndex - openIndexesSeen;
      return closedIndex + openIndexesToSee;
    } else {
      openIndexesSeen += difference;
    }
  }
}


function getOpenIndexCount() {
  let openIndexCount = 0;
  let difference;

  const leftOpenIndexesLength = leftOpenIndexes.length;

  for (let index = 0; index < leftOpenIndexesLength; index++) {
    difference = rightOpenIndexes[index] - leftOpenIndexes[index] + 1;
    openIndexCount += difference;
  }

  return openIndexCount;
}


function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}


// function placeCircle(index, r, w, h, gridSize, maxDistSq) {
function placeCircle(r, w, h, gridSize, maxDistSq) {
  let xClosedLeft, xClosedRight;
  let iClosedLeft, iClosedRight;
  let iOpenLeft, iOpenRight;

  let newLeftOpenIndexes = [];
  let newRightOpenIndexes = [];

  let index;
  let mx, my;

  let yDiffSq;

  index = getRandomOpenIndex();

  // index = 15;

  mx = index % w;
  my = Math.floor(index / w);

  if (getFirstIClosedLeft(my, r, h, mx, maxDistSq, w) != 0) {
    newLeftOpenIndexes.push(0);
  }

  for (let y = max(0, my - r); y < min(h, my + r + 1); y++) {
    yDiffSq = (my - y) ** 2;

    xClosedLeft = getXClosedLeft(mx, r, yDiffSq, maxDistSq);
    xClosedRight = getXClosedRight(h, mx, r, yDiffSq, maxDistSq);


    if (drawing) {
      // Figure out if this is inlined in C.
      // const x1 = xClosedLeft;
      // const y1 = y;
      // const x2 = xClosedRight + 1;
      // const y2 = y + 1;
      drawRect(xClosedLeft, y, xClosedRight + 1, y + 1, w, h);
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

  circlesPlaced++;

  combineOpenIndexes(newLeftOpenIndexes, newRightOpenIndexes, w, h, gridSize);
}


function getFirstIClosedLeft(my, r, h, mx, maxDistSq, w) {
  if (max(0, my - r) < min(h, my + r + 1)) {
    const firstY = max(0, my - r);
    const yDiffSq = (my - firstY) ** 2;
    const xClosedLeft = getXClosedLeft(mx, r, yDiffSq, maxDistSq);
    const iClosedLeft = xToIndex(xClosedLeft, firstY, w);
    // console.log(y, yDiffSq, xClosedLeft, iClosedLeft);
    return iClosedLeft;
  }
}


function getLastIClosedRight(my, r, h, mx, maxDistSq, w) {
  if (max(0, my - r) < min(h, my + r + 1)) {
    const lastY = min(h, my + r + 1) - 1;
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

  xLeft = max(0, mx - r);

  // TODO: Replace with smart math to instantly calculate xLeft and xRight that fit inside of the circle.
  distLeftSq = (mx - xLeft) ** 2 + yDiffSq;
  while (distLeftSq > maxDistSq) { // TODO: May loop infinitely due to my - y?
    xLeft++;
    distLeftSq = (mx - xLeft) ** 2 + yDiffSq;
  }

  return xLeft;
}


function getXClosedRight(h, mx, r, yDiffSq, maxDistSq) {
  let xRight, distRightSq;

  xRight = min(h - 1, mx + r);

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

  let oldIndex = 0,
    newIndex = 0;

  let start, end;

  let combinedLeftOpenIndexes = [];
  let combinedRightOpenIndexes = [];

  while (oldIndex < oldOpenIndexesLength) {
    start = max(oldLeftOpenIndexes[oldIndex], newLeftOpenIndexes[newIndex]);
    end = min(oldRightOpenIndexes[oldIndex], newRightOpenIndexes[newIndex]);

    if (end >= start) {
      combinedLeftOpenIndexes.push(start);
      combinedRightOpenIndexes.push(end);
    }

    if (newIndex + 1 <= newOpenIndexesLength && newLeftOpenIndexes[newIndex + 1] <= oldRightOpenIndexes[oldIndex]) {
      newIndex++;
    } else {
      oldIndex++;
    }
  }

  leftOpenIndexes = [...combinedLeftOpenIndexes];
  rightOpenIndexes = [...combinedRightOpenIndexes];

  // console.log(leftOpenIndexes, rightOpenIndexes);
}


function initDrawGrid() {
  const size = min(innerWidth - 1, innerHeight - 1);
  createCanvas(size, size);

  // rectMode(RADIUS);
  rectMode(CORNERS);
  // ellipseMode(RADIUS);

  noSmooth();

  stroke(175, 50, 50);
  fill(175, 50, 50);
}


function drawRect(x1, y1, x2, y2, w, h) {
  const widthMult = width / w;
  const heightMult = height / h;
  rect(x1 * widthMult, y1 * heightMult, x2 * widthMult, y2 * heightMult);
  // square(mx * width / w, my * height / h, r * width / w);
  // circle(mx * width / w, my * height / h, r * width / w);
}


// USER SETTINGS //
const circleCount = 1;
const w = 256; // Width of grid.
const h = 256; // Height of grid.
const r = 3; // Radius of circle, 0 means a single cell.
const placeSpeedMultiplier = 10;
///////////////////


const gridSize = w * h;
let colorIndex = 0;
const maxDistSq = r ** 2;


function setup() {
  initDrawGrid();

  initOpenIndexes(gridSize);

  // placeCircle(0, r, w, h, gridSize, maxDistSq);
  // placeCircle(7, r, w, h, gridSize, maxDistSq);

  // Test the corners.
  // placeCircle(0, 0, r, w, h, gridSize);
  // placeCircle(4, 0, r, w, h, gridSize);
  // placeCircle(0, 4, r, w, h, gridSize);
  // placeCircle(4, 4, r, w, h, gridSize);
}


function draw() {
  const colors = [
    [50, 50, 200],
    [50, 200, 50],
    [50, 200, 200],
    [200, 50, 50],
    [200, 50, 200],
    [200, 200, 50],
    [200, 200, 200],
  ];

  let chosenColor;

  if (frameCount % 1 == 0) {
    chosenColor = colors[colorIndex++ % colors.length];
    fill(chosenColor);
    stroke(chosenColor);

    for (let i = 0; i < placeSpeedMultiplier; i++) {
      if (leftOpenIndexes.length != 0) {
        placeCircle(r, w, h, gridSize, maxDistSq);
        placed++;
      }
    }
  }

  if (frameCount % 60 == 0) {
    console.log(`open: ${leftOpenIndexes.length}, placed/IRL second: ${placed/((performance.now()-prevTime)/1000)}`);
    placed = 0;
    prevTime = performance.now();
  }
}