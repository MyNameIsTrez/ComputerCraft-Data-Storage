#include <stdio.h>

void setPixel(int x, int y) {
	printf("x: %d, y: %d\n", x, y);
}

void plotCircle1(int xm, int ym, int r)
{
	setPixel(xm, ym);
	int x = -r, y = 0, err = 2-2*r; /* II. Quadrant */ 
	do {
		setPixel(xm-x, ym+y); /*   I. Quadrant */
		setPixel(xm-y, ym-x); /*  II. Quadrant */
		setPixel(xm+x, ym-y); /* III. Quadrant */
		setPixel(xm+y, ym+x); /*  IV. Quadrant */
		r = err;
		if (r <= y) err += ++y*2+1;           /* e_xy+e_y < 0 */
		if (r > x || err > y) err += ++x*2+1; /* e_xy+e_x > 0 or no 2nd y-step */
	} while (x < 0);
}

void plotCircle2(int x0, int y0, int radius)
{
    int x = radius;
    int y = 0;
    int xChange = 1 - (radius << 1);
    int yChange = 0;
    int radiusError = 0;

    while (x >= y)
    {
        for (int i = x0 - x; i <= x0 + x; i++)
        {
            setPixel(i, y0 + y);
            setPixel(i, y0 - y);
        }
        for (int i = x0 - y; i <= x0 + y; i++)
        {
            setPixel(i, y0 + x);
            setPixel(i, y0 - x);
        }

        y++;
        radiusError += yChange;
        yChange += 2;
        if (((radiusError << 1) + xChange) > 0)
        {
            x--;
            radiusError += xChange;
            xChange += 2;
        }
    }
}

void plotCircle3(int mx, int my, int radius) {
	for(int y=-radius; y<=radius; y++)
		for(int x=-radius; x<=radius; x++)
			if(x*x+y*y <= radius*radius)
				setPixel(mx+x, my+y);
}

void set3DPixel(int x, int y, int z) {
	printf("x: %d, y: %d, z: %d\n", x, y, z);
}

void plot3DCircle3(int mx, int my, int mz, int radius) {
	for(int z=-radius; z<=radius; z++)
		for(int y=-radius; y<=radius; y++)
			for(int x=-radius; x<=radius; x++)
				if(x*x+y*y+z*z <= radius*radius*radius)
					set3DPixel(mx+x, my+y, mz+z);
}

int main(void) {
	/*
	plotCircle1(5, 5, 2);
	//printf("\n");
	//plotCircle2(5, 5, 2);
	printf("\n");
	plotCircle3(5, 5, 2);
	*/
	plot3DCircle3(5, 5, 5, 2);

	return 1;
}
