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


function placeCircle(r, w, h, gridSize, maxDistSq) {
  let xLeft, xRight; // Combined they mean the range of closed cells on a y-slice of the circle.
  let iLeft, iRight;

  let newLeftRemovedIndexes = [];
  let newRightRemovedIndexes = [];

  let index;
  let mx, my;

  let yDiffSq;
  let distLeftSq, distRightSq;

  index = getRandomOpenIndex();

  // index = 36;

  // console.log(index);

  mx = index % w;
  my = Math.floor(index / w);

  // console.log(`mx: ${mx}, my: ${my}`);

  // TODO: For simplicity this is assuming a square, but a circle would be more accurate.
  // m stands for middle.
  for (let y = max(0, my - r); y < min(h, my + r + 1); y++) { // TODO: my + r instead?
    xLeft = max(0, mx - r);

    yDiffSq = (my - y) ** 2;

    // TODO: Replace with smart math to instantly calculate xLeft and xRight that fit inside of the circle.
    distLeftSq = (mx - xLeft) ** 2 + yDiffSq;
    while (distLeftSq > maxDistSq) { // TODO: May loop infinitely due to my - y?
      xLeft++;
      distLeftSq = (mx - xLeft) ** 2 + (my - y) ** 2;
    }

    xRight = min(h - 1, mx + r); // TODO: mx + r - 1 instead?

    distRightSq = (xRight - mx) ** 2 + yDiffSq;

    // console.log(`initial xRight: ${xRight}, (xRight - mx) ** 2: ${(xRight - mx) ** 2}, yDiffSq: ${yDiffSq}, distRightSq: ${distRightSq}`);

    while (distRightSq > maxDistSq) {
      xRight--;
      distRightSq = (xRight - mx) ** 2 + yDiffSq;
    }

    iLeft = xLeft + y * w;
    iRight = xRight + y * w;

    newLeftRemovedIndexes.push(iLeft);
    newRightRemovedIndexes.push(iRight);

    // console.log(`y: ${y}, xLeft: ${xLeft}, xRight: ${xRight}, iLeft: ${iLeft}, iRight: ${iRight}`);

    const x1 = xLeft;
    const y1 = y;
    const x2 = xRight + 1;
    const y2 = y + 1;
    drawRect(x1, y1, x2, y2, w, h);
  }

  circlesPlaced++;

  combineRemovedIndexes(newLeftRemovedIndexes, newRightRemovedIndexes, w, h);
  calcOpenIndexes(gridSize);
}


/*
 ** Combines the ranges of removed indexes.
 ** For example, [5, 7] means index 5, 6 and 7 are removed.
 **
 ** [             ] + [[5,6], [9,10]] = [[5,6], [9,10]         ]
 ** [[5,6], [9,10]] + [[2,3], [6, 7]] = [[2,3], [5, 7], [9, 10]]
 */
function combineRemovedIndexes(newLeftRemovedIndexes, newRightRemovedIndexes, w, h) {
  let newLeftIsSmallest;
  let newIndex = 0;
  let oldIndex = 0;
  let combinedLeftRemovedIndexes, combinedRightRemovedIndexes;

  const newLeftRemovedIndexesLength = newLeftRemovedIndexes.length;
  const oldLeftRemovedIndexesLength = leftRemovedIndexes.length;

  let newLeftRemovedIndex, oldLeftRemovedIndex;
  let newRightRemovedIndex, oldRightRemovedIndex;

  let minLeft;
  let minRight = 0;

  if (circlesPlaced == 1) { // Copy.
    leftRemovedIndexes = [...newLeftRemovedIndexes];
    rightRemovedIndexes = [...newRightRemovedIndexes];
  } else { // Combines leftRemovedIndexes and newLeftRemovedIndexes.

    // TODO: A pretty big optimization would be to reuse this array somehow.
    combinedLeftRemovedIndexes = [];
    combinedRightRemovedIndexes = [];

    // Initialize minLeft to the smallest left index.
    minLeft = min(newLeftRemovedIndexes[0], leftRemovedIndexes[0]);

    for (let combinedIndex = 0; combinedIndex < newLeftRemovedIndexesLength + oldLeftRemovedIndexesLength; combinedIndex++) {
      // console.log(`newIndex: ${newIndex}, oldIndex: ${oldIndex}`);

      newLeftRemovedIndex = newIndex == newLeftRemovedIndexesLength ? Infinity : newLeftRemovedIndexes[newIndex];
      oldLeftRemovedIndex = oldIndex == oldLeftRemovedIndexesLength ? Infinity : leftRemovedIndexes[oldIndex];

      newLeftIsSmallest = newLeftRemovedIndex < oldLeftRemovedIndex;

      if (newLeftIsSmallest) {
        newRightRemovedIndex = newRightRemovedIndexes[newIndex];

        // If newLeftRemovedIndex = 2 and minRight = 1 then this for-loop isn't entered.
        // This is because in this example these ranges should be combined,
        // as there are no open spots between these closed ranges.
        if (combinedIndex > 0 && newLeftRemovedIndex > minRight + 1) {
          combinedLeftRemovedIndexes.push(minLeft);
          combinedRightRemovedIndexes.push(minRight);

          minLeft = newLeftRemovedIndex;
        }

        minRight = max(minRight, newRightRemovedIndex);

        newIndex++;
      } else {
        oldRightRemovedIndex = rightRemovedIndexes[oldIndex];

        if (combinedIndex > 0 && oldLeftRemovedIndex > minRight + 1) {
          combinedLeftRemovedIndexes.push(minLeft);
          combinedRightRemovedIndexes.push(minRight);

          minLeft = oldLeftRemovedIndex;
        }

        minRight = max(minRight, oldRightRemovedIndex);

        oldIndex++;
      }
    }

    combinedLeftRemovedIndexes.push(minLeft);
    combinedRightRemovedIndexes.push(minRight);

    // TODO: Copy unnecessary?
    leftRemovedIndexes = [...combinedLeftRemovedIndexes];
    rightRemovedIndexes = [...combinedRightRemovedIndexes];
  }

  // console.log(leftRemovedIndexes, rightRemovedIndexes);
}


// Gets openIndexes by inversing removedIndexes.
function calcOpenIndexes(gridSize) {
  let leftRemovedIndex; // TODO: Default value?
  let prevRightRemovedIndex; // TODO: Default to 0?

  const leftRemovedIndexesLength = leftRemovedIndexes.length;
  const rightRemovedIndexesLength = rightRemovedIndexes.length;

  let firstRemovedIndex, lastRemovedIndex;

  // TODO: A pretty big optimization would be to reuse this array somehow.
  leftOpenIndexes = [];
  rightOpenIndexes = [];

  firstRemovedIndex = leftRemovedIndexes[0];
  if (firstRemovedIndex != 0) {
    leftOpenIndexes.push(0);
    rightOpenIndexes.push(firstRemovedIndex - 1);
  }

  for (let removedIndexesIndex = 0; removedIndexesIndex < leftRemovedIndexesLength; removedIndexesIndex++) {
    // There will always be open spaces between leftRemovedIndex and prevRightRemovedIndex, the code below just figures out from where to where.
    leftRemovedIndex = leftRemovedIndexes[removedIndexesIndex];

    if (removedIndexesIndex > 0) {
      leftOpenIndexes.push(prevRightRemovedIndex + 1);
      rightOpenIndexes.push(leftRemovedIndex - 1);
    }

    prevRightRemovedIndex = rightRemovedIndexes[removedIndexesIndex];
  }

  lastRemovedIndex = rightRemovedIndexes[rightRemovedIndexesLength - 1];
  if (lastRemovedIndex != gridSize - 1) {
    leftOpenIndexes.push(lastRemovedIndex + 1);
    rightOpenIndexes.push(gridSize - 1);
  }

  // console.log(leftOpenIndexes, rightOpenIndexes);
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
const w = 256; // Width of grid.
const h = 256; // Height of grid.
const r = 4; // Radius of circle, 0 means a single cell.
const placeSpeedMultiplier = 1;
///////////////////


const gridSize = w * h;
let colorIndex = 0;
const maxDistSq = r ** 2;


function setup() {
  initDrawGrid();

  initOpenIndexes(gridSize);

  // console.log("\n".repeat(100));

  // placeCircle(r, w, h, gridSize, maxDistSq);
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

  if (frameCount % 2 == 0) {
    const chosenColor = colors[colorIndex++ % colors.length];
    fill(chosenColor);
    stroke(chosenColor);

    for (let i = 0; i < placeSpeedMultiplier; i++) {
      if (leftOpenIndexes.length != 0) {
        placeCircle(r, w, h, gridSize, maxDistSq);
      }
    }
  }
}