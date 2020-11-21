#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

int getScore(const int desiredCircleCount, int circles[]) {
	int smallestDiff = INT_MAX;

	int r1, g1, b1, r2, g2, b2;
	/*
	int rDiff, gDiff, bDiff;
	int rDiffSq, gDiffSq, bDiffSq;
	int rAvg;
	*/
	int rWeight = 1, gWeight = 1, bWeight = 1;
	int diff;

	for (int i = 0; i < (desiredCircleCount - 1) * 3; i += 3) {
		for (int j = i + 1; j < desiredCircleCount * 3; j += 3) {
			r1 = circles[i + 0];
			g1 = circles[i + 1];
			b1 = circles[i + 2];

			r2 = circles[j + 0];
			g2 = circles[j + 1];
			b2 = circles[j + 2];

			/*
			rDiff = r1 - r2;
			gDiff = g1 - g2;
			bDiff = b1 - b2;
			
			rDiffSq = rDiff * rDiff;
			gDiffSq = gDiff * gDiff;
			bDiffSq = bDiff * bDiff;

			rAvg = (r1 + r2) / 2;
			
			rWeight = (2 + rAvg / 256) * rDiffSq;
			gWeight = 4 * gDiffSq;
			bWeight = (2 + (255 - rAvg) / 256) * bDiffSq;
			*/

			for (int i = 0; i < 3; i++) {
				rWeight *= (r1 - r2);
				gWeight *= (g1 - g2);
				bWeight *= (b1 - b2);
			}

			diff = rWeight + gWeight + bWeight;

			if (diff < smallestDiff) {
				smallestDiff = diff;
			}
		}	
	}

	printf("smallestDiff: %d\n", smallestDiff);
	return smallestDiff;
}

void close(const int x, const int y, const int z, const int w, const int h, const int d, int *open, int arr1[], int arr2[]) {
	if (x >= 0 && x < w && y >= 0 && y < h && z >= 0 && z < d) {
		const int n1 = x + y * w + z * (w * h);

		if (n1 >= 0) { // TODO: If-statement is probably redundant.
			const int arr1i1 = arr2[n1];
			
			if (arr1i1 < *open - 1) {
				const int arr1i2 = *open - 1;
				const int n2 = arr1[arr1i2];

				// arr1 editing
				arr1[arr1i1] = n2;
				arr1[arr1i2] = n1;

				// arr2 editing
				arr2[n1] = arr1i2;
				arr2[n2] = arr1i1;

				(*open)--;
			} else if (arr1i1 == *open - 1) {
				(*open)--;
			} else {} // When it's already been removed.
		}
	}
}

void reset(const int cellCount, int arr1[], int arr2[], int *circlesPlaced, int *open) {
	for (int i = 0; i < cellCount; i++) {
		arr1[i] = i;
		arr2[i] = i;
	}
	*circlesPlaced = 0;
	*open = cellCount;
}

double rand01(void) {
	return rand() / ((double) RAND_MAX);
}

int getRandomOpen(int arr1[], const int *open) {
	return arr1[(int)(rand01() * (*open))];
}

// Find faster algorithm, because this checks every cell in a cube.
void placeCircle(int arr1[], int arr2[], int *open, const int w, const int h, const int d, const int diameter, int circles[], int circlesPlaced) {
	const int i = getRandomOpen(arr1, open);

	const int mx = i % w;
	const int my = i / w;
	const int mz = i / (w * h);

	circles[circlesPlaced * 3 + 0] = mx;
	circles[circlesPlaced * 3 + 1] = my;
	circles[circlesPlaced * 3 + 2] = mz;

	const int radius = diameter;

	for(int z=-radius; z<=radius; z++)
		for(int y=-radius; y<=radius; y++)
			for(int x=-radius; x<=radius; x++)
				if(x*x+y*y+z*z <= radius*radius*radius)
					close(mx+x, my+y, mz+z, w, h, d, open, arr1, arr2);
}

// TODO: Check Wikipedia page to see if this implementation is correct.
// https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
// https://stackoverflow.com/a/14976268/13279557
/*
void placeCircle(int arr1[], int arr2[], int *open, const int w, const int h, const int d, const int diameter, int circles[], int circlesPlaced) {
	const int i = getRandomOpen(arr1, open);

	const int x0 = i % w;
	const int y0 = i / w;
	const int z0 = i / (w * h);

	circles[circlesPlaced * 3 + 0] = x0;
	circles[circlesPlaced * 3 + 1] = y0;
	circles[circlesPlaced * 3 + 2] = z0;

	const int radius = diameter;

	int x = radius;
	int y = 0;
	int xChange = 1 - (radius << 1); // TODO: Is the automatic cast to int unwanted?
	int yChange = 0;
	int radiusError = 0;

	while (x >= y) {
		for (int i = x0 - x; i <= x0 + x; i++) {
			// TODO: REWRITE THIS WHOLE FUNCTION SO IT'S FOR 3D
			close(i, y0 + y, z, w, h, d, open, arr1, arr2);
			close(i, y0 - y, z, w, h, d, open, arr1, arr2);
		}
		for (int i = x0 - y; i <= x0 + y; i++) {
			close(i, y0 + x, z, w, h, d, open, arr1, arr2);
			close(i, y0 - x, z, w, h, d, open, arr1, arr2);
		}

		y++;
		radiusError += yChange;
		yChange += 2;
		
		if (((radiusError << 1) + xChange) > 0) {
			x--;
			radiusError += xChange;
			xChange += 2;
		}
	}
}
*/

int main(void) {
	// CONFIGURABLE
	const int desiredCircleCount = 94;
	const int w = 256;
	const int h = 256;
	const int d = 256;
	const char fileName[] = "palette.txt";


	// NOT CONFIGURABLE
	const int cellCount = w * h * d;
	
	int *arr1;
	int *arr2;
	arr1 = malloc(cellCount * sizeof(int));
	arr2 = malloc(cellCount * sizeof(int));
	
	int circlesPlaced;
	int circlesPlacedTotal;

	int open;
	int circles[desiredCircleCount * 3];
	int diameter = 0;
	int score;
	int highScore = 0;
	FILE *fpw;
	FILE *fpr;
	
	clock_t startTime, endTime;
	float totalTime;


	// TODO: Read highScore from file and use that as a starting point.
	highScore = 0;
	
	fpr = fopen(fileName, "r");
	if (fpr != NULL) {
		fscanf(fpr, "%d", &circlesPlacedTotal);
		fclose(fpr);
	} else {
		circlesPlacedTotal = 0;
	}

	// TODO: Read startTime from file and use that as a starting point.
	startTime = clock();

	while (1) {
		reset(cellCount, arr1, arr2, &circlesPlaced, &open);

		while (circlesPlaced < desiredCircleCount) {
			if (open > 0) {
				placeCircle(arr1, arr2, &open, w, h, d, diameter, circles, circlesPlaced);
				circlesPlaced++;
				circlesPlacedTotal++;
			} else { // This will probably never happen.
				reset(cellCount, arr1, arr2, &circlesPlaced, &open);
			}
		}

		score = getScore(desiredCircleCount, circles);

		if (score > highScore) {
			printf("highscore!");
			endTime = clock();
			totalTime = (float)(endTime - startTime) / CLOCKS_PER_SEC;
			
			diameter = (int)(sqrt(score));
			highScore = score;

			fpw = fopen(fileName, "w");
			if (fpw == NULL) {
				printf("Error getting write handle.");
			}

			fprintf(fpw, "%d\n", circlesPlacedTotal);
			fprintf(fpw, "%d\n", score);
			fprintf(fpw, "%f\n", totalTime);

			printf("%d score after %d circles were placed in total, found after %f seconds\n", score, circlesPlacedTotal, totalTime);

			for (int j = 0; j < desiredCircleCount * 3; j++) {
				fprintf(fpw, "%d", circles[j]);
				if (j != desiredCircleCount * 3 - 1) {
					fprintf(fpw, ", ");
				}
			}

			fclose(fpw);
		}
	}

	free(arr1);
	free(arr2);

	return 0;
}
