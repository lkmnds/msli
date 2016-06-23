
FLAGS=-std=c99 -Wall

LIBS=-lreadline -lm

FILES=src/main.c	\
	src/parser.c	\

msl:
	mkdir out
	cc $(FLAGS) $(FILES) $(LIBS) -o out/msl

all: msl
