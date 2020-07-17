
#include "ambiente.h"

myambiente *createAmbiente( int *size){
	myambiente *new = NULL;
	int **dados = NULL;
	int **matriz = NULL;
	new = (myambiente *) malloc ( sizeof(myambiente));
	dados = (int **) malloc ( size[0]*sizeof(int *));
	matriz = (int **) malloc ( size[0]*sizeof(int *));
	for (int i = 0; i < size[0]; i++) {
		dados[i] = (int *) malloc (size[1]*sizeof(int));
		matriz[i] = (int *) malloc (size[1]*sizeof(int));
	}
	zeraAmbiente( dados, matriz, size);
	new->dados = dados;
	new->matriz = matriz;
	new->linhas = size[0];
	new->colunas = size[1];

	return new;
}


void zeraAmbiente( int **dados, int **matriz, int *size){
	for(i = 0; i < size[0]; i++){
		for( j = 0; j < size[1]; j++){
			dados[i][j] = 0;
			matriz[i][j] = 0;
		}
	}
}

bool contaItens( myexperimento *experimento){
	bool resp = false;
	int nItens[ experimento->nGrupos];
	int this;

	myambiente *ambiente = experimento->ambiente;
	formiga *formigas = experimento->formigas;
	itens *itens = experimento->itens;
	for(int i; i < experimento->nGrupos; i++)
		nItens[i] = 0;
	for( int i = 0; i < ambiente->linhas; i++){
		for (int j = 0; j < ambiente->colunas; j++) {
			if (( ambiente->matriz[i][j] == ITEM) || (ambiente->matriz[i][j] == ITEMFORMIGA)) {
				this = itens[ ambiente->dados[i][j]]->grupo;
				nItens[this]++;
			}
		}
	}
	for( int i = 0; i < experimento->nFormigas; i++){
		if( formigas[i]->carry){
			this = itens[formigas[i]->carga]->grupo;
			nItens[this]++;
		}
	}
	return resp;
}