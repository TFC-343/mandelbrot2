# mandelbrot2
Requires python 3.9 and Pygame 2
main.py shows the Mandelbrot set and lets you zoom in used in white box, to change the resolution open in a text editor and go to line 17,
change the number to the size of the pixel (a larger number would be fewer pixels overall)

line 65 is Mandelbrot equation
z = z**2 + num -> Z_(n-1)= (Z_n)^2 + C
you can change this to change the Mandelbrot result for example you can change is to:
z = z**2 + 1/num  for an inverse Mandelbrot set

julia set.py: I’m almost sure this isn’t called a Julia set but that’s what I’m calling it here,
it used the same equation but Z_0 is equal to the position and C is a constant, you can change this constant be clicking on the screen

julia set with movemnt.py has a far lower resolution but will change in real time as you move your mouse.
