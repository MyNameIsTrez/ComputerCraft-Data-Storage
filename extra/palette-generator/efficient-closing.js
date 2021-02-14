////////////////////
// TODO: In C these globals should be replaced and be passed by address.
let circlesPlaced = 0;

let leftRemovedIndexes = [];
let rightRemovedIndexes = [];

let leftOpenIndexes = [];
let rightOpenIndexes = [];
////////////////////


function initFlat(flat, w, h) {
  for (let i = 0; i < w * h; i++) {
    flat[i] = i;
  }
}


function placeCircle(mx, my, flat, r, w, h, gridSize) {
  let xLeft, xRight; // Combined they mean the range of closed cells on a y-slice of the circle.
  let iLeft, iRight;

  let newLeftRemovedIndexes = [];
  let newRightRemovedIndexes = [];

  // TODO: For simplicity this is assuming a square, but a circle would be more accurate.
  // m stands for middle.
  for (let y = max(0, my - r); y < min(h - 1, my + r); y++) {
    xLeft = max(0, mx - r);
    xRight = min(h - 1, mx + r - 1);

    iLeft = xLeft + y * w;
    iRight = xRight + y * w;

    newLeftRemovedIndexes.push(iLeft);
    newRightRemovedIndexes.push(iRight);

    // console.log(`y: ${y}, xLeft: ${xLeft}, xRight: ${xRight}, iLeft: ${iLeft}, iRight: ${iRight}`);
  }

  circlesPlaced++;

  combineRemovedIndexes(newLeftRemovedIndexes, newRightRemovedIndexes);
  calcOpenIndexes(gridSize);
}


/*
 ** Combines the ranges of removed indexes.
 ** For example, [5, 7] means index 5, 6 and 7 are removed.
 **
 ** [             ] + [[5,6], [9,10]] = [[5,6], [9,10]         ]
 ** [[5,6], [9,10]] + [[2,3], [6, 7]] = [[2,3], [5, 7], [9, 10]]
 */
function combineRemovedIndexes(newLeftRemovedIndexes, newRightRemovedIndexes) {
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

        // If newLeftRemovedIndex = 2 and minRight = 1 then this for-loop shouldn't be entered.
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

  console.log(leftRemovedIndexes, rightRemovedIndexes);
}


// Gets openIndexes by inversing removedIndexes.
function calcOpenIndexes(gridSize) {
  
}


function setup() {
  // USER SETTINGS //
  const w = 4; // Width of grid.
  const h = 4; // Height of grid.
  const r = 1; // Radius of circle.
  ///////////////////


  let flat = [];
  const gridSize = w * h;


  initFlat(flat, w, h);

  placeCircle(2, 2, flat, r, w, h, gridSize);
  placeCircle(3, 1, flat, r, w, h, gridSize);
  placeCircle(1, 1, flat, r, w, h, gridSize);
  // placeCircle(0, 0, flat, r, w, h, gridSize);
}