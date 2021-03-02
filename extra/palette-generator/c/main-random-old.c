#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

void	skip_rand(int n)
{
	while (n > 0)
	{
		rand();
		n--;
	}
}

void	generate_colors(int color_count)
{
	char	file_name[] = "palette.txt";
	FILE	*fp_r;
	FILE	*fp_w;

	int	colors[color_count * 3];

	double	score;
	double	high_score;

	double	r1, g1, b1, r2, g2, b2;
	
	double	r_diff, g_diff, b_diff;
	double	r_diff_sq, g_diff_sq, b_diff_sq;

	double	avg_r;
	
	double	r_weight, g_weight, b_weight;
	double	diff;

	int	gens;
	int	gens_done;

	clock_t	start_t;
	clock_t	end_t;
	float	total_t;

	colors[0]  = 0;
	colors[1]  = 0;
	colors[2]  = 0;

	colors[3]  = 0;
	colors[4]  = 0;
	colors[5]  = 255;
	
	colors[6]  = 0;
	colors[7]  = 255;
	colors[8]  = 0;
	
	colors[9]  = 0;
	colors[10] = 255;
	colors[11] = 255;
	
	colors[12] = 255;
	colors[13] = 0;
	colors[14] = 0;
	
	colors[15] = 255;
	colors[16] = 0;
	colors[17] = 255;
	
	colors[18] = 255;
	colors[19] = 255;
	colors[20] = 0;
	
	colors[21] = 255;
	colors[22] = 255;
	colors[23] = 255;

	high_score = 0;
	
	gens = 1;

	if ((fp_r = fopen(file_name, "r")) != NULL)
	{
		fscanf(fp_r, "%d", &gens_done);
		
		while (gens < gens_done)
		{
			skip_rand(color_count * 3 - 8 * 3);
			gens++;
		}
	}

	start_t = clock();

	while (1)
	{
		for (int k = 8 * 3; k < color_count * 3; k++) {
			colors[k] = rand() % 256;
		}

		score = INT_MAX;

		for (int i = 0; i < color_count - 1; i++) {
			for (int j = i + 1; j < color_count; j++) {
				r1 = colors[i * 3 + 0];
				g1 = colors[i * 3 + 1];
				b1 = colors[i * 3 + 2];
	
				r2 = colors[j * 3 + 0];
				g2 = colors[j * 3 + 1];
				b2 = colors[j * 3 + 2];

				r_diff = r1 - r2;
				g_diff = g1 - g2;
				b_diff = b1 - b2;
				
				r_diff_sq = r_diff * r_diff;
				g_diff_sq = g_diff * g_diff;
				b_diff_sq = b_diff * b_diff;

				avg_r = (r1 + r2) / 2;
				
				r_weight = (2 + avg_r / 256) * r_diff_sq;
				g_weight = 4 * g_diff_sq;
				b_weight = (2 + (255 - avg_r) / 256) * b_diff_sq;
				
				diff = r_weight + g_weight + b_weight;

				if (diff < score) {
					score = diff;
				}
			}
		}
	
		if (score > high_score)
		{
			end_t = clock();
			total_t = (float)(end_t - start_t) / CLOCKS_PER_SEC;
			
			high_score = score;

			if ((fp_w = fopen(file_name, "w")) == NULL) {
				printf("Error getting write handle.");
			}

			fprintf(fp_w, "%d\n", gens);
			fprintf(fp_w, "%f\n", score);
			fprintf(fp_w, "%f\n", total_t);

			printf("%f score after %d circles were placed in total, found after %f seconds since the start\n", score, gens * color_count, total_t);

			for (int j = 0; j < color_count * 3; j++) {
				fprintf(fp_w, "%d", colors[j]);
				if (j != color_count * 3 - 1) {
					fprintf(fp_w, ", ");
				}
			}

			fclose(fp_w);
		}

		gens++;
	}
}

int	main(void)
{
	int	color_count = 94;

	generate_colors(color_count);

	return (0);
}
