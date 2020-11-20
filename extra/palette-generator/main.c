#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>

int getScore(int desiredCircleCount, int circles[]) {
	int smallestDiff = INT_MAX;

	int r1, g1, b1, r2, g2, b2;
	int rDiff, gDiff, bDiff;
	int rDiffSq, gDiffSq, bDiffSq;
	int rAvg;
	int rWeight, gWeight, bWeight;
	int diff;

	for (int i = 0; i < (desiredCircleCount - 1) * 3; i += 3) {
		for (int j = i + 1; j < desiredCircleCount * 3; j += 3) {
			r1 = circles[i + 0];
			g1 = circles[i + 1];
			b1 = circles[i + 2];

			r2 = circles[j + 0];
			g2 = circles[j + 1];
			b2 = circles[j + 2];

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
			
			diff = rWeight + gWeight + bWeight;

			if (diff < smallestDiff) {
				smallestDiff = diff;
			}
		}	
	}

	return smallestDiff;
}

int main(void) {
	// CONFIGURABLE
	int desiredCircleCount = 94;
	int w = 256;
	int h = 256;
	char fileName[] = "palette.txt";
	

	// NOT CONFIGURABLE
	int cellCount = w * h;
	int arr1[cellCount];
	int arr2[cellCount];
	
	int circlesPlaced;
	int circlesPlacedTotal;

	int open;
	int circles[desiredCircleCount * 3];
	int diameter = 0;
	int score;
	int highScore = 0;
	int recordCircles[desiredCircleCount * 3];
	FILE *fpw;
	
	clock_t startTime, endTime;
	float totalTime;


	// TODO: Read highScore from file and use that as a starting point.
	highScore = 0;
	
	FILE *fpr = fopen(fileName, "r");
	if (fpr != NULL) {
		fscanf(fpr, "%d", &circlesPlacedTotal);
	} else {
		circlesPlacedTotal = 0;
	}
	fclose(fpr);

	// TODO: Read startTime from file and use that as a starting point.
	startTime = clock();

	while (1) {
		// TODO: Put this in a "reset" function.
		for (int i = 0; i < cellCount; i++) {
			arr1[i] = i;
			arr2[i] = i;
		}
		circlesPlaced = 0;
		open = cellCount;

		while (circlesPlaced < desiredCircleCount) {
			circlesPlaced++;
			circlesPlacedTotal++;
		}

		score = getScore(desiredCircleCount, circles);

		if (score > highScore) {
			endTime = clock();
			totalTime = (float)(endTime - startTime) / CLOCKS_PER_SEC;
			
			highScore = score;

			fpw = fopen(fileName, "w");
			if (fpw == NULL) {
				printf("Error getting write handle.");
			}

			fprintf(fpw, "%d\n", circlesPlacedTotal);
			fprintf(fpw, "%d\n", score);
			fprintf(fpw, "%f\n", totalTime);

			printf("%d score after %d circles were placed in total, found after %f seconds\n", score, circlesPlacedTotal, totalTime);

			for (j = 0; j < desiredCircleCount * 3; j++) {
				fprintf(fpw, "%d", circles[j]);
				if (j != desiredCircleCount * 3 - 1) {
					fprintf(fpw, ", ");
				}
			}

			fclose(fpw);
		}
	}
	
	return 0;
}
