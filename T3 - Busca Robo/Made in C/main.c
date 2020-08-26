#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ambiente.h"
#include "robo.h"

int main( int argc, char *argv[]){
	FILE *file = NULL;
	ambiente myambiente;
	int linha = 1, coluna = 1;
	//printf("HELLO WORLD!\n");

	if (argc != 2) {
		printf("MAIN >> ERROR: PARÂMETROS INCORRETOS\n");
		exit(1);
	}
	file = fopen( argv[1], "r");
	if (file == NULL){
		printf("MAIN >> ERROR: ABERTURA DO ARQUIVO\n");
		exit(1);
	}
	contaLinCol ( file, &linha, &coluna, ' ');
	fclose(file);
	//printf("Numero de Linhas: %i\nNumero de Colunas: %i\n", linha, coluna);
	file = fopen( argv[1], "r");
	if (file == NULL){
		printf("MAIN >> ERROR: ABERTURA DO ARQUIVO\n");
		exit(1);
	}
	myambiente.matriz = NULL;
	myambiente.lin = linha;
	myambiente.col = coluna;
	if (malocar(&myambiente)){
		printf("MAIN >> ERROR: OUT OF MEMORY!\n");
	}
	getAmbiente( myambiente.matriz, file, linha, coluna);
	fclose(file);
	mimprimir( &myambiente);
	setPesoField( &myambiente);
	system("clear");
	mimprimir(&myambiente);
	return 1;
}