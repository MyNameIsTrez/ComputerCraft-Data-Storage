function runTests() {
    w = 5;
    h = 5;
    r = 1;
    
    gridSize = w * h;
    maxDistSq = r ** 2;

    
    testOne(2, [], []);


    // INDIVIDUAL //

    // Corners.
    testOne(0, [2, 6], [4, 24]); // 1
    testOne(4, [0, 5, 10], [2, 8, 24]); // 2
    testOne(20, [0, 16, 22], [14, 19, 24]); // 3
    testOne(24, [0, 20], [18, 22]); // 4
    
    // Middle.
    testOne(12, [0, 8, 14, 18], [6, 10, 16, 24]); // 5


    // COMBINED //
    
    if (allTestsPassed) {
        clear();
        initOpenIndexes();
    }

    // Corners.
    
    test(0, [2, 6], [4, 24]); // 6
    test(4, [2, 6, 10], [2, 8, 24]); // 7
    test(20, [2, 6, 10, 16, 22], [2, 8, 14, 19, 24]); // 8
    test(24, [2, 6, 10, 16, 22], [2, 8, 14, 18, 22]); // 9

    // Middle.
    test(12, [2, 6, 8, 10, 14, 16, 18, 22], [2, 6, 8, 10, 14, 16, 18, 22]); // 10


    // TEMPLATE //

    // test(, [], []);


    if (allTestsPassed) {
        console.log("All tests passed! 🎉");
        clear();
    }
}


function testOne(index, expectedLeftOpenIndexes, expectedRightOpenIndexes) {
    if (allTestsPassed) {
        clear();
        initOpenIndexes();
        test(index, expectedLeftOpenIndexes, expectedRightOpenIndexes);
    }
}


function test(index, expectedLeftOpenIndexes, expectedRightOpenIndexes) {
    if (allTestsPassed) {
        placeCircle(index, r, w, h, gridSize, maxDistSq);
        drawIndexesText();
        testNumber++;
        assertTest(leftOpenIndexes, expectedLeftOpenIndexes, rightOpenIndexes, expectedRightOpenIndexes);
    }
}


function drawIndexesText() {
    for (let index = 0; index < gridSize; index++) {
        drawCenteredText(index);
    }
}


function drawCenteredText(index) {
    const mx = index % w;
    const my = Math.floor(index / w);
    const widthMult = width / w;
    const heightMult = height / h;
    const x = (mx + 0.5) * widthMult;
    const y = (my + 0.5) * heightMult;

    push();
    noStroke();
    fill(255);
    text(index, x, y);
    pop();
}


function arraysEqual(a1,a2) {
    /* WARNING: Arrays must not contain {objects} or behavior may be undefined. */
    return JSON.stringify(a1) === JSON.stringify(a2);
}


function assertTest(leftOpenIndexes, expectedLeftOpenIndexes, rightOpenIndexes, expectedRightOpenIndexes) {
    const leftEqual = arraysEqual(leftOpenIndexes, expectedLeftOpenIndexes);
    const rightEqual = arraysEqual(rightOpenIndexes, expectedRightOpenIndexes);

    if (!leftEqual || !rightEqual) {
        allTestsPassed = false;

        console.log(`Test ${testNumber} failed!`);

        console.log(`\nexpected left: ${expectedLeftOpenIndexes}`);
        console.log(`expected right: ${expectedRightOpenIndexes}`);
        
        console.log(`\nleft: ${leftOpenIndexes}`);
        console.log(`right: ${rightOpenIndexes}`);
    }
}