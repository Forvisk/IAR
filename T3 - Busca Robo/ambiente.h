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

#endif

int malocar( ambiente *amb);

int splitFirst (const char *str, char sep, int nLin, int *vetNum);
int split(const char *str, char sep, int nLin, int *vetNum);
int contaLinCol ( FILE *file, int *linha, int *coluna, char sep);
char *getLinha( FILE *const file);
int mimprimir( ambiente *myambiente);

ambiente *geraambiente( int lin, int col);
int getAmbiente( int **matriz, FILE *file, int lin, int col);