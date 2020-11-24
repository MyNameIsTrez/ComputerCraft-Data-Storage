#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

void getScore(const int desiredCircleCount, int circles[], double *score, int *distScore) {
	*score = INT_MAX;

	double r1, g1, b1, r2, g2, b2;

	double rDiff, gDiff, bDiff;
	double rDiffSq, gDiffSq, bDiffSq;

	double rAvg;

	double rWeight, gWeight, bWeight;
	double diff;

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
			
			rWeight = (2 + rAvg / 256) * rDiffSq;         // min: 2 * rDiffSq, max: (2 + 255/256) * rDiffSq
			gWeight = 4 * gDiffSq;                        // min & max: 4 * gDiffSq
			bWeight = (2 + (255 - rAvg) / 256) * bDiffSq; // min: (2 + 255/256) * bDiffSq, max: 2 * bDiffSq
			
			/*
			// Simple euclidean distance. Doesn't reflect how eyes work.
			rWeight = (r1 - r2) * (r1 - r2);
			gWeight = (g1 - g2) * (g1 - g2);
			bWeight = (b1 - b2) * (b1 - b2);
			*/

			diff = rWeight + gWeight + bWeight;

			if (diff < *score) {
				*score = diff;
				*distScore = sqrt(rDiffSq + gDiffSq + bDiffSq);
			}
		}	
	}
}

void close(const int x, const int y, const int z, const int w, const int wh, int *open, int arr1[], int arr2[]) {
	const int n1 = x + y * w + z * wh;
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
	} // else {} // When it has already been removed.
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
	return rand() / (double)RAND_MAX;
}

int getRandomOpen(int arr1[], const int *open) {
	return arr1[(int)(rand01() * (*open))];
}

// Find faster algorithm, because this checks every cell in the shape of a cube, instead of a sphere.
void placeCircle(int arr1[], int arr2[], int *open, const int w, const int h, const int d, const int wh, const int dist, const int distSq, int circles[], const int circlesPlacedIdx) {
	const int i = getRandomOpen(arr1, open);

	const int mx = i % w;
	const int my = (i / w) % h;
	const int mz = i / (w * h);

	circles[circlesPlacedIdx + 0] = mx;
	circles[circlesPlacedIdx + 1] = my;
	circles[circlesPlacedIdx + 2] = mz;

	//printf("mx: %d, my: %d, mz: %d\n", mx, my, mz);

	const int zMin = mz - dist < 0     ?   - mz     : -dist;
	const int zMax = mz + dist > d - 1 ? d - mz - 1 :  dist;
	const int yMin = my - dist < 0     ?   - my     : -dist;
	const int yMax = my + dist > h - 1 ? h - my - 1 :  dist;
	const int xMin = mx - dist < 0     ?   - mx     : -dist;
	const int xMax = mx + dist > w - 1 ? w - mx - 1 :  dist;

	for(int z = zMin; z <= zMax; z++)
		for(int y = yMin; y <= yMax; y++)
			for(int x = xMin; x <= xMax; x++)
				if(x*x+y*y+z*z <= distSq)
					close(mx+x, my+y, mz+z, w, wh, open, arr1, arr2);
}

int main(void) {
	// CONFIGURABLE
	const int desiredCircleCount = 94;

	const int w = 256;
	const int h = 256;
	const int d = 256;

	const char fileName[] = "palette.txt";

	// NOT CONFIGURABLE
	const int wh = w * h;
	const int cellCount = w * h * d;
	
	int *arr1;
	int *arr2;
	arr1 = malloc(cellCount * sizeof(int));
	arr2 = malloc(cellCount * sizeof(int));
	
	int circlesPlaced;
	int circlesPlacedTotal;

	int open;
	int circles[desiredCircleCount * 3];

	double highScore = 0;
	double score;

	int dist = 0;
	int distScore;
	int distSq = 0;

	FILE *fpw;
	FILE *fpr;

	clock_t startTime, endTime, offsetTime = 0;
	int flooredTime;

	fpr = fopen(fileName, "r");
	if (fpr != NULL) {
		fscanf(fpr, "%lf %d %d %ld", &highScore, &dist, &circlesPlacedTotal, &offsetTime);
		fclose(fpr);
		printf("LOADED: ");
		printf("%d high score with a distance of %d after %d circles were placed in total, found after %d seconds since the start\n", (int)highScore, dist, circlesPlacedTotal, (int)(offsetTime / (double)CLOCKS_PER_SEC));
	} else {
		circlesPlacedTotal = 0;
		highScore = 0;
	}

	//highScore = 0;

	startTime = clock();

	while (1) {
		reset(cellCount, arr1, arr2, &circlesPlaced, &open);

		while (circlesPlaced < desiredCircleCount) {
			if (open > 0) {
				placeCircle(arr1, arr2, &open, w, h, d, wh, dist, distSq, circles, circlesPlaced * 3);
				circlesPlaced++;
				circlesPlacedTotal++;
//				if (circlesPlaced % 2 == 0) {
//					printf("circlesPlaced++\n");
//				} else {
//					printf("circlesPlaced++!\n");
//				}
			} else {
//				printf("EARLY RESET!!!\n");
				reset(cellCount, arr1, arr2, &circlesPlaced, &open);
			}
		}

		getScore(desiredCircleCount, circles, &score, &distScore);

//		printf("score: %lf, highScore: %lf\n", score, highScore);
		if (score > highScore) {
			highScore = score;

			dist = distScore; // TODO: Use better heuristic.
			distSq = dist * dist;

			fpw = fopen(fileName, "w");
			if (fpw == NULL) {
				printf("Error getting write handle.");
			}

			fprintf(fpw, "%lf\n%d\n%d\n%ld\n", highScore, dist, circlesPlacedTotal, endTime + offsetTime - startTime);

			endTime = clock();
			flooredTime = (endTime + offsetTime - startTime) / CLOCKS_PER_SEC;

			printf("%d high score with a distance of %d after %d circles were placed in total, found after %d seconds since the start\n", (int)highScore, dist, circlesPlacedTotal, flooredTime);

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
