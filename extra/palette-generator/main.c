#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>

int getSmallestDiff(int desiredCircleCount, int colors[]) {
	int smallestDiff = INT_MAX;

	int r1, g1, b1, r2, g2, b2;
	int rDiff, gDiff, bDiff;
	int rDiffSq, gDiffSq, bDiffSq;
	int rAvg;
	int rWeight, gWeight, bWeight;
	int diff;

	for (int i = 0; i < (desiredCircleCount - 1) * 3; i += 3) {
		for (int j = i + 1; j < desiredCircleCount * 3; j += 3) {
			r1 = colors[i + 0];
			g1 = colors[i + 1];
			b1 = colors[i + 2];

			r2 = colors[j + 0];
			g2 = colors[j + 1];
			b2 = colors[j + 2];

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
	int desiredCircleCount = 94;
	char fileName[] = "palette.txt";
	
	FILE *fpw;
	
	clock_t startTime, endTime;
	float totalTime;
	
	int circlesPlaced;
	int circlesPlacedTotal;

	int colors[desiredCircleCount * 3];

	int smallestDiff, largestDiff;

	// TODO: Read largestDiff from file and use that as a starting point.
	largestDiff = 0;
	
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

		smallestDiff = getSmallestDiff(desiredCircleCount, colors);

		if (smallestDiff > largestDiff) {
			endTime = clock();
			totalTime = (float)(endTime - startTime) / CLOCKS_PER_SEC;
			
			largestDiff = smallestDiff;

			fpw = fopen(fileName, "w");
			if (fpw == NULL) {
				printf("Error getting write handle.");
			}

			fprintf(fpw, "%d\n", circlesPlacedTotal);
			fprintf(fpw, "%d\n", smallestDiff);
			fprintf(fpw, "%f\n", totalTime);

			printf("%d score after %d circles were placed in total, found after %f seconds\n", smallestDiff, circlesPlacedTotal, totalTime);

			for (j = 0; j < desiredCircleCount * 3; j++) {
				fprintf(fpw, "%d", colors[j]);
				if (j != desiredCircleCount * 3 - 1) {
					fprintf(fpw, ", ");
				}
			}

			fclose(fpw);
		}
	}
	
	return 0;
}
