all:
	gcc -Wall -Wextra -Wshadow -pedantic -o mlt3 mlt3.c

clean:
	rm -f mlt3
