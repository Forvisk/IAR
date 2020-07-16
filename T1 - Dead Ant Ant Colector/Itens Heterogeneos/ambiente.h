#ifndef __AMBIENTE_H
#define __AMBIENTE_H

#include <stdlib.h>
#include <stdio.h>
#include <stdlib.h>

#define VAZIO 0
#define ITEM 1
#define FORMIGA 2
#define ITEMFORMIGA 3

// ambiente
typedef struct{
	int **dados;
	int **matriz;
	int linhas;
	int colunas;
} myambiente;

// formigas
typedef struct {
	int posX;
	int posY;
	bool carry;
	int carga;
} formiga;

typedef struct {
	float *dado;
	int grupo;
} item;

typedef struct {
	int nGrupos;
	int size[2];
	int *nItensG;
	int nFormigas;
	int raioVisao;
	item *itens;
	formiga *formigas;
	ambiente ambiente;
} myexperimento;

myambiente *createAmbiente(int *size);
void zeraAmbiente( int **dados, int **matriz, int *size);

float distancia(int pos1[2], int pos2[2]);
float distanciaVizinhanca( int pos[2]);

bool contaItens( myexperimento *experimento);

void mover( formiga *this, myambiente *ambiente);
void pegarItem( formiga *this, myambiente *ambiente);
void largarItem( formiga *this, myambiente *ambiente);

#endif