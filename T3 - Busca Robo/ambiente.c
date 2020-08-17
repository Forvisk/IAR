#include "ambiente.h"

int malocar (ambiente *amb) {
	int **newMatriz = NULL;

	newMatriz = (int **) malloc(amb->lin*sizeof(int *));
	if (!newMatriz) {
		printf("ERROR: Out of memory\n");
		return 1;
	}
	for (int i =0; i < amb->lin; i++) {
			newMatriz[i] = (int *) malloc(sizeof(int)*amb->col);
			if (!newMatriz) {
				printf("ERROR: Out of memory\n");
				return 1;
			}
	}
	for (int i = 0; i < amb->lin; i++)
		for (int j = 0; j < amb->col; j++)
		{
			newMatriz[i][j] = 0;
		}

	amb->matriz = newMatriz;
	return 0;
}

int splitFirst (const char *str, char sep, int nLin, int *vetNum){
	int conta_num = 0, len = 0;
	unsigned int start = 0, stop = 0;
	char *tmpStr = NULL;
	int *tmpVet = NULL;

	tmpVet = (int *) malloc (strlen(str) * sizeof(int));
	if (tmpVet == NULL) printf("splitFirst >> ERROR: OUT OF MEMORY\n");

	for ( stop = 0; str[stop]; stop++) {
		
		if (str[stop] == sep) {
			tmpStr = (char *) calloc (12, sizeof(char));
			if (tmpStr == NULL) printf("splitFirst >> ERROR: OUT OF MEMORY\n");
			if (stop - start > 10) printf("splitFirst >> ERROR: QUANTOS TERRENOS VOCÊ ESTACOLOCANDO NESSA COISA!!!!\n");
			memcpy (tmpStr, str + start, stop - start);

			tmpVet[conta_num] = atoi(tmpStr);
			free(tmpStr);
			conta_num++;
			start = stop + 1;
		} else if (str[stop] == '\0') printf("splitFirst >> Fim da leitura da linha %i\n", nLin);
	}
	len = conta_num;
	vetNum = (int *) malloc (len * sizeof(int));
	if (vetNum == NULL) printf("splitFirst >> ERROR: OUT OF MEMORY\n");

	for (conta_num = 0; conta_num < len; ++conta_num)	{
		vetNum[conta_num] = tmpVet[conta_num];
	}
	if (tmpStr == NULL) printf("split >> ERROR: OUT OF MEMORY\n");
	strncpy(tmpStr, str + start, stop - start);
	free(tmpVet);
	return len;
}

int split(const char *str, char sep, int nLin, int *vetNum){
	int conta_num = 0;
	unsigned int start = 0, stop = 0;
	char *tmpStr = NULL;
	for ( stop = 0; str[stop]; stop++) {
		if ((str[stop] == sep) || (str[stop] == '\n') || (str[stop] == '\0')) {
			tmpStr = (char *) calloc (12, sizeof(char));
			if (tmpStr == NULL) printf("split >> ERROR: OUT OF MEMORY\n");
			if (stop - start > 10) printf("split >> ERROR: QUANTOS TERRENOS VOCÊ ESTACOLOCANDO NESSA COISA!!!!\n");
			memcpy(tmpStr, str + start, stop - start);

			vetNum[conta_num] = atoi(tmpStr);
			free(tmpStr);
			conta_num++;
			start = stop + 1;
		} //else if (str[stop] == '\n') printf("split >> Fim da leitura da linha %i\n", nLin);
	}
	if (tmpStr == NULL) printf("split >> ERROR: OUT OF MEMORY\n");
	strncpy(tmpStr, str + start, stop - start);
	return 0;
}

int contaLinCol ( FILE *file, int *linha, int *coluna, char sep){
	int lin = 1, col = 0;
	char c = fgetc(file);

	while ( c != EOF){
		if ((lin == 1) && (c == sep)){
			col++;
		} else if ((lin == 1) && (c == '\n'))
			col++;
		if (c == '\n'){
			lin++;
		}
		c = fgetc(file);
	}
	//printf("%i %i\n", lin, col);
	*linha = lin;
	*coluna = col;
	return 0;
}

char *getLinha( FILE *file){
	int nChar = 0, i = 0;
	char c = '0';
	char *strAux = NULL;
	//printf("getLinha\n");
	strAux = (char *) malloc (sizeof(char)*100);
	//printf("getLinha-2\n");	
	while ((c != '\n') && !feof(file)){
		//printf("%c", c);
		nChar++;
		//strAux = (char *) realloc(strAux, nChar);
		c = fgetc(file);
		strAux[i] = c;
		i++;
		//printf("%s\n", strAux);
	}
	//printf("\n");
	return strAux;
}

int mimprimir( ambiente *myambiente){
	printf("##### IMPRIMINDO AMBIENTE #####\n");
	printf("\n");
	printf("Linhas: %i\nColunas: %i\n", myambiente->lin, myambiente->col);
	for (int i = 0; i < myambiente->lin; i++){
		for (int j = 0; j < myambiente->col; j++) {
			printf("%2i", myambiente->matriz[i][j]);
		}
		printf("\n");
	}
	printf("######## FIM IMPRESSÃO ########\n");
	return 0;
}

int getAmbiente( int **matriz, FILE *file, int linha, int coluna){
	char *getLine = NULL;
	int tmpVet[coluna];

	for (int i = 0; i < linha; i++)
		for (int j = 0; j < coluna; j++)
			matriz[i][j] = 0;

	for( int i = 0; i < linha; i++){
		//printf("Linha %i de %i\n", i+1, linha);
		//printf("Aqui\n");
		//printf("Aqui2\n");
		getLine = getLinha(file);

		//printf("%s\n", getLine);
		split( getLine, ' ', i+1, tmpVet);
		for (int j = 0; j < coluna; j++){
			matriz[i][j] = tmpVet[j];
			//printf("%i ", matriz[i][j]);
		}
		//printf("\n");
		free(getLine);
	}
	return 0;
}

int setPesoField( ambiente *amb){
	int peso[5] = {1, 5, 10, 15};

	for (int i = 0; i < amb->lin; i++){
		for (int j = 0; j < amb->col; j++)
		{
			amb->matriz[i][j] = peso[amb->matriz[i][j]];
		}
	}
	return 0;
}