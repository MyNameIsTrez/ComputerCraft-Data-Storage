////////////////////
// TODO: In C these globals should be replaced and be passed by address.
let circlesPlaced = 0;

let leftRemovedIndexes = [];
let rightRemovedIndexes = [];

let leftOpenIndexes = [];
let rightOpenIndexes = [];
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


function placeCircle(index, r, w, h, gridSize, maxDistSq) {
  let xClosedLeft, xClosedRight;
  let iClosedLeft, iClosedRight;
  let iOpenLeft, iOpenRight;

  let newLeftOpenIndexes = [];
  let newRightOpenIndexes = [];

  // let index;
  let mx, my;

  let yDiffSq;

  // index = getRandomOpenIndex();

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
    
    
    const x1 = xClosedLeft;
    const y1 = y;
    const x2 = xClosedRight + 1;
    const y2 = y + 1;
    drawRect(x1, y1, x2, y2, w, h);
    

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
 ** Combines the ranges of removed indexes.
 ** For example, [5, 7] means index 5, 6 and 7 are removed.
 **
 ** [             ] + [[5,6], [9,10]] = [[5,6], [9,10]         ]
 ** [[5,6], [9,10]] + [[2,3], [6, 7]] = [[2,3], [5, 7], [9, 10]]
 */
function combineOpenIndexes(newLeftOpenIndexes, newRightOpenIndexes, w, h, gridSize) {
  // console.log(newLeftOpenIndexes, newRightOpenIndexes);

  console.log(leftOpenIndexes, rightOpenIndexes);
}


function initDrawGrid() {
  const size = min(innerWidth - 1, innerHeight - 1);
  createCanvas(size, size);

  //   stroke(200);
  //   fill(50, 200, 50);
  //   // fill(240, 240, 240);
  //   for (let y = 0; y < h; y++) {
  //     for (let x = 0; x < w; x++) {
  //       square(x * width / w, y * height / h, width / w);
  //     }
  //   }

  // rectMode(RADIUS);
  rectMode(CORNERS);
  // ellipseMode(RADIUS);

  noSmooth();

  stroke(175, 50, 50);
  fill(175, 50, 50);
}


function drawRect(x1, y1, x2, y2, w, h) {
  // if (isClosed(x + y * w)) {
  // }
  const widthMult = width / w;
  const heightMult = height / h;
  rect(x1 * widthMult, y1 * heightMult, x2 * widthMult, y2 * heightMult);
  // square(mx * width / w, my * height / h, r * width / w);
  // circle(mx * width / w, my * height / h, r * width / w);
}


function isClosed(index) {
  const leftRemovedIndexesLength = leftRemovedIndexes.length;

  let leftRemovedIndex, rightRemovedIndex;

  for (let removedIndexesIndex = 0; removedIndexesIndex < leftRemovedIndexesLength; removedIndexesIndex++) {
    leftRemovedIndex = leftRemovedIndexes[removedIndexesIndex];
    rightRemovedIndex = rightRemovedIndexes[removedIndexesIndex];

    if (index >= leftRemovedIndex && index <= rightRemovedIndex) {
      return true;
    }
  }

  return false;
}


// USER SETTINGS //
const circleCount = 1;
const w = 4; // Width of grid.
const h = 4; // Height of grid.
const r = 1; // Radius of circle, 0 means a single cell.
const placeSpeedMultiplier = 1;
///////////////////


const gridSize = w * h;
let colorIndex = 0;
const maxDistSq = r ** 2;


function setup() {
  initDrawGrid();

  initOpenIndexes(gridSize);

  // console.log("\n".repeat(100));

  placeCircle(0, r, w, h, gridSize, maxDistSq);
  placeCircle(3, r, w, h, gridSize, maxDistSq);
  placeCircle(12, r, w, h, gridSize, maxDistSq);
  placeCircle(15, r, w, h, gridSize, maxDistSq);
  // placeCircle(r, w, h, gridSize, maxDistSq);

  // for (let i = 0; i < circleCount; i++) {
  //   placeCircle(r, w, h, gridSize);
  //   // console.log(leftOpenIndexes);
  // }

  // drawGrid(w, h);


  // console.log(leftOpenIndexes, rightOpenIndexes);
  // console.log(getRandomOpenIndex());

  // placeCircle(2, 2, r, w, h, gridSize);
  // placeCircle(3, 1, r, w, h, gridSize);
  // placeCircle(1, 1, r, w, h, gridSize);
  // placeCircle(4, 4, r, w, h, gridSize);
  // placeCircle(0, 4, r, w, h, gridSize);
  // placeCircle(0, 0, r, w, h, gridSize);

  // Test the corners.
  // placeCircle(0, 0, r, w, h, gridSize);
  // placeCircle(4, 0, r, w, h, gridSize);
  // placeCircle(0, 4, r, w, h, gridSize);
  // placeCircle(4, 4, r, w, h, gridSize);
  // console.log(getRandomOpenIndex());  
}


// function draw() {
//   const colors = [
//     [50, 50, 200],
//     [50, 200, 50],
//     [50, 200, 200],
//     [200, 50, 50],
//     [200, 50, 200],
//     [200, 200, 50],
//     [200, 200, 200],
//   ];

//   if (frameCount % 2 == 0) {
//     const chosenColor = colors[colorIndex++ % colors.length];
//     fill(chosenColor);
//     stroke(chosenColor);

//     for (let i = 0; i < placeSpeedMultiplier; i++) {
//       if (leftOpenIndexes.length != 0) {
//         placeCircle(r, w, h, gridSize, maxDistSq);
//       }
//     }
//   }
// }