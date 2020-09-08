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
	FILE	*fp_r;
	FILE	*fp_w;
	int	colors[color_count * 3];
	int	i;
	int	smallest_diff;
	int	largest_diff;
	int	idx1;
	int	idx2;
	int	clr1_r;
	int	clr1_g;
	int	clr1_b;
	int	clr2_r;
	int	clr2_g;
	int	clr2_b;
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

	if ((fp_r = fopen("palette.txt", "r")) != NULL)
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
					clr1_r = colors[idx1 + 0];
					clr1_g = colors[idx1 + 1];
					clr1_b = colors[idx1 + 2];
		
					clr2_r = colors[idx2 + 0];
					clr2_g = colors[idx2 + 1];
					clr2_b = colors[idx2 + 2];
		
					diff =
						(clr1_r - clr2_r) * (clr1_r - clr2_r) +
						(clr1_g - clr2_g) * (clr1_g - clr2_g) +
						(clr1_b - clr2_b) * (clr1_b - clr2_b);
		
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

			largest_diff = smallest_diff;

			if ((fp_w = fopen("palette.txt", "w")) == NULL)
				printf("Error getting write handle.");

			fprintf(fp_w, "%d\n", gens);

			total_t = (float)(end_t - start_t) / CLOCKS_PER_SEC;

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
