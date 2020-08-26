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

typedef struct{
	int x;
	int y;
	int distancia;
	int nCaminhos;
	struct noLargura *anterior;
	struct noLargura *caminho;
} noLargura;

#endif

int inicializaRobo(ambiente *amb);

/*Funcoes Busca Largura*/
int buscaLargura (ambiente *amb, int *posIni, int *posFim);

int djkistra(ambiente *amb, int *posIni, int *posFim);
