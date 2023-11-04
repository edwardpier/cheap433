all: rx rx2

rx.o: rx.cc
	g++ -c  rx.cc 

rx: rx.o
	g++ -o rx rx.o -lpigpio

rx2.o: rx2.cc
	g++ -c  rx2.cc 

rx2: rx2.o
	g++ -o rx2 rx2.o -lpigpio	