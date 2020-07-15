#ifndef __AMBIENTE_H
#define __AMBIENTE_H

#include <stdlib.h>

// ambiente
typedef struct{
	float **dados;
	int **ambiente;
	int linhas;
	int colunas;
} ambiente;

// formigas
typedef struct {
	int posX;
	int posY;
	bool carry;
	float *carga;
} formiga;

typedef struct {
	float *dado;
	int grupo;
} item;

ambiente *createAmbiente();

float distancia(int pos1[2], int pos2[2]);
float distanciaVizinhanca( int pos[2]);



#endif