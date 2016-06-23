
FLAGS=-std=c99 -Wall

LIBS=-lreadline -lm

FILES=src/main.c	\
	src/parser.c	\
	src/ast.c		\

msl:
	mkdir -p out
	cc -g $(FLAGS) $(FILES) $(LIBS) -o out/msl

all: msl
