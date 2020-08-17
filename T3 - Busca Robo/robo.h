#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef SOME_HEADER_FILE_H
#define SOME_HEADER_FILE_H

typedef struct {
	int **matriz;
	int lin;
	int col;
} ambiente;

typedef struct{
	int x;
	int y;
	struct movimento *next;
	struct movimento *last;
	int pontos;
} movimento;

#endif

int inicializaRobo(ambiente *amb);
