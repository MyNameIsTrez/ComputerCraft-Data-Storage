#include <stdlib.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>

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

	int	i;

	int	smallest_diff;
	int	largest_diff;

	int	idx1;
	int	idx2;

	int	r1;
	int	g1;
	int	b1;

	int	r2;
	int	g2;
	int	b2;
	
	int	r_diff;
	int	g_diff;
	int	b_diff;
	
	int	r_diff_sq;
	int	g_diff_sq;
	int	b_diff_sq;

	int	avg_r;
	
	int	r_weight;
	int	g_weight;
	int	b_weight;

	int	diff;
	int	gens;
	int	j;
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

	largest_diff = 0;
	
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
		i = 8 * 3;
		while (i < color_count * 3)
		{
			colors[i] = rand() % 256;
			i++;
		}

		idx1 = 0;
		smallest_diff = INT_MAX;

		while (idx1 < (color_count - 1) * 3)
		{
			idx2 = 0;
			
			while (idx2 < color_count * 3)
			{
				if (idx1 != idx2)
				{
					r1 = colors[idx1 + 0];
					g1 = colors[idx1 + 1];
					b1 = colors[idx1 + 2];
		
					r2 = colors[idx2 + 0];
					g2 = colors[idx2 + 1];
					b2 = colors[idx2 + 2];

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

					if (diff < smallest_diff)
						smallest_diff = diff;
				}

				idx2 += 3;
			}
	
			idx1 += 3;
		}
	
		if (smallest_diff > largest_diff)
		{
			end_t = clock();
			total_t = (float)(end_t - start_t) / CLOCKS_PER_SEC;
			
			largest_diff = smallest_diff;

			if ((fp_w = fopen(file_name, "w")) == NULL)
				printf("Error getting write handle.");

			fprintf(fp_w, "%d\n", gens);
			fprintf(fp_w, "%d\n", smallest_diff);
			fprintf(fp_w, "%f\n", total_t);

			printf("%d score at gen %d, found after %f seconds\n", smallest_diff, gens, total_t);

			j = 0;
			while (j < color_count * 3)
			{
				fprintf(fp_w, "%d", colors[j]);
				if (j != color_count * 3 - 1)
					fprintf(fp_w, ", ");
				j++;
			}

			fclose(fp_w);

			start_t = clock();
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
