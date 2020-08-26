#include "robo.h"


int inicializaRobo(ambiente *amb){
	return 0;
}

int buscaLargura (ambiente *amb, int *posIni, int *posFim){
	noLargura inicio;
	int menorDistancia = 0;
	int **PesoCaminho;
	noLargura *expande = NULL;
	noLargura *nextExpande = NULL;
	noLargura *menorCaminho = NULL;

	noLargura *new = NULL;
	int nExpande = 1, nNextExpande = 0;
	int novosEx = 0;
	int finaliza = 0;
	int first = 1;


	inicio.x = posIni[0]-1;
	inicio.y = posIni[1]-1;
	inicio.anterior = NULL;
	inicio.caminho = NULL;
	inicio.nCaminhos = 0;
	inicio.distancia = 0;

	PesoCaminho = (int **) malloc(amb->lin * sizeof(int *));
	for (int i = 0; i < amb->lin; i++){
		PesoCaminho[i] = (int *) malloc (amb->col * sizeof(int));
		for (int j; j < amb->col; j++)
			PesoCaminho[i][j] = 0;
	}
	expande = (noLargura *) malloc (nExpande * sizeof(noLargura));
	/* Expande o primeiro nó*/
	if( inicio.x - 1 >= 0){
		PesoCaminho[inicio.x -1][inicio.y] += amb->matriz[inicio.x -1][inicio.y];
		inicio.nCaminhos++;
		if(first == 1){
			new = expande[0];
		}else
	}
	if ( inicio.x +1 < amb->lin){
		PesoCaminho[inicio.x +1][inicio.y] += amb->matriz[inicio.x +1][inicio.y];
	}
	if( inicio.y -1 >= 0){
		PesoCaminho[inicio.x][inicio.y -1] += amb->matriz[inicio.x][inicio.y -1];
	}
	if( inicio.y +1 < amb->col){
		PesoCaminho[inicio.x][inicio.y +1] += amb->matriz[inicio.x][inicio.y +1];
	}
	
	
	expande[0] = &inicio;
	while( finaliza == 0){
		for (int i = 0; i < nExpande; i++){
			/*Expande o nó*/
		}
	}

	/* Libera memória */
	for( int j = 0; j < amb->col; j++)
		free(PesoCaminho[i]);
	free(PesoCaminho);

	return menorDistancia;
}