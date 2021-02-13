#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>
#include <math.h>


double getScore(const int desiredCircleCount, int circles[]) {
	double r1, g1, b1, r2, g2, b2;

	double rDiff, gDiff, bDiff;
	double rDiffSq, gDiffSq, bDiffSq;

	double rAvg;

	double rWeight, gWeight, bWeight;

	double diff;
	double score = INT_MAX;

	for (int i = 0; i < desiredCircleCount - 1; i++) {
		for (int j = i + 1; j < desiredCircleCount; j++) {
			r1 = circles[i * 3 + 0];
			g1 = circles[i * 3 + 1];
			b1 = circles[i * 3 + 2];

			r2 = circles[j * 3 + 0];
			g2 = circles[j * 3 + 1];
			b2 = circles[j * 3 + 2];

			
			rDiff = r1 - r2;
			gDiff = g1 - g2;
			bDiff = b1 - b2;
			
			rDiffSq = rDiff * rDiff;
			gDiffSq = gDiff * gDiff;
			bDiffSq = bDiff * bDiff;

			rAvg = (r1 + r2) / 2;
			
			rWeight = (2 + rAvg / 256) * rDiffSq;         // min:  2 * rDiffSq           , max: (2 + 255/256) * rDiffSq
			gWeight = 4 * gDiffSq;                        // min:  4 * gDiffSq           , max:  4 * gDiffSq
			bWeight = (2 + (255 - rAvg) / 256) * bDiffSq; // min: (2 + 255/256) * bDiffSq, max:  2 * bDiffSq


			/*
			// Simple euclidean distance. Doesn't mimic how human eyes perceive color.
			rWeight = (r1 - r2) * (r1 - r2);
			gWeight = (g1 - g2) * (g1 - g2);
			bWeight = (b1 - b2) * (b1 - b2);
			*/


			diff = rWeight + gWeight + bWeight;

			score = fmin(score, diff);
		}
	}

	return score;
}


/*
** Values in flat are (X,Y,Z) coordinates mapped to 1D.
** flatIndexes[n] returns the index of value n in flat.
**
** closeCoord is the value in flat that is to be closed.
** closeCoordIndex is the index of closeCoord in flat.
**
** lastOpenCoord is the value of the last open cell in flat.
** lastOpenCoordIndex is the index of the last open cell in flat.
**
** The algorithm is similar to this one, except that "Scratch" and "Result" are combined into a single array:
** https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#Modern_method
*/
void close(const int x, const int y, const int z, const int w, const int wh, int *open, int flat[], int flatIndexes[]) {
	const int closeCoord = x + y * w + z * wh;
	const int closeCoordIndex = flatIndexes[closeCoord];

	if (closeCoordIndex < *open - 1) {
		const int lastOpenCoordIndex = *open - 1;
		const int lastOpenCoord = flat[lastOpenCoordIndex];

		flat[closeCoordIndex] = lastOpenCoord;
		// flat[lastOpenCoordIndex] = closeCoord; // An unnecessary step as this coord is being closed.

		flatIndexes[closeCoord] = lastOpenCoordIndex;
		flatIndexes[lastOpenCoord] = closeCoordIndex;

		(*open)--;
	} else if (closeCoordIndex == *open - 1) {
		(*open)--;
	} // else {} // When it has already been removed.
}


void reset(const int cellCount, int flat[], int flatIndexes[], int *circlesPlaced, int *open) {
	for (int i = 0; i < cellCount; i++) {
		flat[i] = i;
		flatIndexes[i] = i;
	}

	*circlesPlaced = 0;
	*open = cellCount;
}


double randNormalized(void) {
	return rand() / (double)RAND_MAX;
}


int getRandomOpen(int flat[], const int *open) {
	return flat[(int)(randNormalized() * (*open))];
}


void placeCircle(int flat[], int flatIndexes[], int *open, const int w, const int h, const int d, const int wh, const int dist, const int distSq, int circles[], const int circlesPlacedIdx) {
	const int i = getRandomOpen(flat, open);

	const int mx = i % w;
	const int my = (i / w) % h;
	const int mz = i / (w * h);

	circles[circlesPlacedIdx + 0] = mx;
	circles[circlesPlacedIdx + 1] = my;
	circles[circlesPlacedIdx + 2] = mz;

	// Prevents trying to close out of bounds coordinates.
	const int zMin = mz - dist < 0     ?   - mz     : - dist;
	const int zMax = mz + dist > d - 1 ? d - mz - 1 :   dist;
	const int yMin = my - dist < 0     ?   - my     : - dist;
	const int yMax = my + dist > h - 1 ? h - my - 1 :   dist;
	const int xMin = mx - dist < 0     ?   - mx     : - dist;
	const int xMax = mx + dist > w - 1 ? w - mx - 1 :   dist;

	// TODO:
	// Optimize this major bottleneck.
	// This currently calls close() around (dist*2)^3 times, so for dist=60 that is 1.7 million times.
	//
	// Looping through the volume of a sphere instead of the volume of a cube would only be 91% faster[1].
	// If done, it has to both still be correct and also faster!
	//
	// [1]: 1/(volumeSphere/volumeCube) = 1/0.524 = 1.91.

	for(int z = zMin; z <= zMax; z++)
		for(int y = yMin; y <= yMax; y++)
			for(int x = xMin; x <= xMax; x++)
				if(x*x + y*y + z*z <= distSq)
					close(mx+x, my+y, mz+z, w, wh, open, flat, flatIndexes);
}


void readRecord(const char fileName[], double *highScore, int startDist, int *dist, int *distSq, int *circlesPlacedTotal, double *secondsOffset) {
	FILE *fpr;

	fpr = fopen(fileName, "r");

	if (fpr != NULL) {
		fscanf(fpr, "%lf %d %d %lf", highScore, dist, circlesPlacedTotal, secondsOffset);
		fclose(fpr);

		printf("-- LOADING --\n");

		printf("Calling rand() %d times...\n", *circlesPlacedTotal);

		// To get deterministic results even when saving and loading multiple times, it'll be necessary for rand() to return the same values.
		// The seed for rand() is always the same, so we just need to call rand() circlesPlacedTotal times to achieve this determinism.
		for (int i = 0; i < *circlesPlacedTotal; i++)
			rand();

		printf("%d high score with a distance of %d after %d circles were placed in total, found after %d seconds since the very start.\n\n", (int)(*highScore), *dist, *circlesPlacedTotal, (int)(*secondsOffset));

		*distSq = (*dist) * (*dist);
	} else {
		*highScore = 0;
		*dist = startDist;
		*distSq = startDist * startDist;
		*circlesPlacedTotal = 0;
		*secondsOffset = 0;
	}
}


void writeRecord(const char fileName[], double highScore, int dist, int circlesPlacedTotal, double secondsElapsed, int desiredCircleCount, int circles[]) {
	FILE *fpw;

	fpw = fopen(fileName, "w");

	if (fpw == NULL) {
		printf("Error getting write handle.");
	}

	fprintf(fpw, "%lf\n%d\n%d\n%lf\n", highScore, dist, circlesPlacedTotal, secondsElapsed);

	for (int j = 0; j < desiredCircleCount * 3; j++) {
		fprintf(fpw, "%d", circles[j]);
		if (j != desiredCircleCount * 3 - 1) {
			fprintf(fpw, ", ");
		}
	}

	fclose(fpw);
}


int main(void) {
	// CONFIGURABLE //
	const int desiredCircleCount = 94; // 94 for ComputerCraft.

	const int w = 256; // Width.
	const int h = 256; // Height.
	const int d = 256; // Depth.

	const char fileName[] = "palette.txt";

	const int startDist = 30;
	//////////////////


	const int wh = w * h;
	const int cellCount = w * h * d;

	int *flat;
	int *flatIndexes;

	flat = malloc(cellCount * sizeof(int));
	flatIndexes = malloc(cellCount * sizeof(int));

	int circlesPlaced, circlesPlacedTotal;

	int open;
	int circles[desiredCircleCount * 3];

	double score, highScore;

	int dist, distSq;

	clock_t startTime;
	double secondsOffset, secondsElapsed;


	readRecord(fileName, &highScore, startDist, &dist, &distSq, &circlesPlacedTotal, &secondsOffset);

	printf("-- RUNNING --\n");

	startTime = clock();

	while (1) {
		reset(cellCount, flat, flatIndexes, &circlesPlaced, &open);

		while (circlesPlaced < desiredCircleCount) {
			if (open > 0) {
				placeCircle(flat, flatIndexes, &open, w, h, d, wh, dist, distSq, circles, circlesPlaced * 3);
				circlesPlaced++;
				circlesPlacedTotal++;
			} else { // Probably never reached, but just in case.
				reset(cellCount, flat, flatIndexes, &circlesPlaced, &open);
			}
		}

		score = getScore(desiredCircleCount, circles);

		if (score > highScore) {
			highScore = score;

			// TODO: Find better heuristic.
			dist++;

			distSq = dist * dist;

			secondsElapsed = (clock() - startTime) / (double)CLOCKS_PER_SEC + secondsOffset;

			writeRecord(fileName, highScore, dist, circlesPlacedTotal, secondsElapsed, desiredCircleCount, circles);

			printf("%d high score with a distance of %d after %d circles were placed in total, found after %d seconds since the very start.\n", (int)highScore, dist, circlesPlacedTotal, (int)secondsElapsed);
		}
	}

	free(flat);
	free(flatIndexes);

	return 0;
}
