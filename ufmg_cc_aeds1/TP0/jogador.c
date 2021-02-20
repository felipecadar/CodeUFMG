#include "jogador.h"
#include <stdio.h>
#include <stdlib.h>

int andar(int vet[], int player, Jogador *play, int **validos){
	int p_maior = 9;

	int tamanho = 8;
	int maior = -100;
	int i;
	int col, lin;
	int p, g;

	
	for (i = 0; i < tamanho; ++i)
	{	
		col = play[player].vizinhos[i][2];
		lin = play[player].vizinhos[i][1];

		if(vet[i] >= maior && vet[i] != 9 && validos[lin][col] == 1 && vet != 0){
			maior = vet[i];
			p_maior = i;
			p = col;
			g = lin;
		}
	}

		if(maior == -100){
		return 404;
		}
	
//	printf("%i\n", maior);
	return p_maior;
}

int pokestop(int vet[], int player, Jogador *play, int **validos){
	int tamanho = 8;
	int maior = -100;
	int i;
	int col, lin;
	int p, g;
	int p_maior = 404;


	
	for (i = 0; i < tamanho; ++i)
	{	
		col = play[player].vizinhos[i][2];
		lin = play[player].vizinhos[i][1];

		if(vet[i] == 0 && vet[i] != 9 && validos[lin][col] != 0){
			maior = vet[i];
			p_maior = i;
			p = col;
			g = lin;
		}
	}


	if(maior != 0){
		return 90;
	}

		if(p_maior == -100){
		return 404;
		}

//	printf("%i\n", maior);
	return p_maior;
}

int semPokestop(int vet[], int player, Jogador *play, int **validos){	int p_maior = 9;

	int tamanho = 8;
	int maior = -100;
	int i;
	int col, lin;
	int p, g;

	
	for (i = 0; i < tamanho; ++i)
	{	
		col = play[player].vizinhos[i][2];
		lin = play[player].vizinhos[i][1];

		if(vet[i] >= maior && vet[i] != 9 && validos[lin][col] == 1 && vet != 0){
			maior = vet[i];
			p_maior = i;
			p = col;
			g = lin;
		}
	}

		if(maior == -100){
		return 404;
		}
	
//	printf("%i\n", maior);
//	printf("%i\n", p_maior);
	return p_maior;

}

int **explorar(Jogador *play, int  i,int  camp,int  **mapa){


	//preenche o valor dos vizinhos
	if( play[i].p_atual[0] - 1  >= 0 && play[i].p_atual[1] - 1  >= 0 && play[i].p_atual[0] - 1  < camp && play[i].p_atual[1] - 1  <camp ){
		play[i].vizinhos[0][0] = mapa[play[i].p_atual[0] - 1 ][play[i].p_atual[1] - 1 ];
		play[i].vizinhos[0][1] = play[i].p_atual[0] - 1;
		play[i].vizinhos[0][2] = play[i].p_atual[1] - 1; 
	}else{
		play[i].vizinhos[0][0] = 9;
		// validos[play[i].vizinhos[0][1]][play[i].vizinhos[0][2]] = 0;
	}

	if(play[i].p_atual[0] - 0  >= 0 && play[i].p_atual[1] - 1  >= 0 && play[i].p_atual[0] - 0  < camp && play[i].p_atual[1] - 1  < camp ){
		play[i].vizinhos[1][0] = mapa[play[i].p_atual[0] - 0 ][play[i].p_atual[1] - 1 ];
		play[i].vizinhos[1][1] = play[i].p_atual[0]; 
		play[i].vizinhos[1][2] = play[i].p_atual[1] -1; 
	}else{
		play[i].vizinhos[1][0] = 9;
		// validos[play[i].vizinhos[1][1]][play[i].vizinhos[1][2]] = 0;

	}

	if(play[i].p_atual[0] + 1  >= 0 && play[i].p_atual[1] - 1  >= 0 && play[i].p_atual[0] + 1  < camp && play[i].p_atual[1] - 1  < camp ){
		play[i].vizinhos[2][0] = mapa[play[i].p_atual[0] + 1 ][play[i].p_atual[1] - 1 ];
		play[i].vizinhos[2][1] = play[i].p_atual[0] +1; 
		play[i].vizinhos[2][2] = play[i].p_atual[1] -1;
	}else{
		play[i].vizinhos[2][0] = 9;
		// validos[play[i].vizinhos[2][1]][play[i].vizinhos[2][2]] = 0;
	}

	if(play[i].p_atual[0] - 1  >= 0 && play[i].p_atual[1] - 0  >= 0 && play[i].p_atual[0] - 1  < camp && play[i].p_atual[1] - 0  < camp ){
		play[i].vizinhos[3][0] = mapa[play[i].p_atual[0] - 1 ][play[i].p_atual[1] - 0 ];
		play[i].vizinhos[3][1] = play[i].p_atual[0] -1; 
		play[i].vizinhos[3][2] = play[i].p_atual[1];
	}else{
		play[i].vizinhos[3][0] = 9;
		// validos[play[i].vizinhos[3][1]][play[i].vizinhos[3][2]] = 0;
	}		
	if(play[i].p_atual[0] + 1  >= 0 && play[i].p_atual[1] - 0  >= 0 && play[i].p_atual[0] + 1  < camp && play[i].p_atual[1] - 0  < camp ){
		play[i].vizinhos[4][0] = mapa[play[i].p_atual[0] + 1 ][play[i].p_atual[1] - 0 ];
		play[i].vizinhos[4][1] = play[i].p_atual[0] +1; 
		play[i].vizinhos[4][2] = play[i].p_atual[1];
	}else{
		play[i].vizinhos[4][0] = 9;
		// validos[play[i].vizinhos[4][1]][play[i].vizinhos[4][2]] = 0;
	}
	if(play[i].p_atual[0] - 1  >= 0 && play[i].p_atual[1] + 1  >= 0 && play[i].p_atual[0] - 1  < camp && play[i].p_atual[1] + 1  < camp ){
		play[i].vizinhos[5][0] = mapa[play[i].p_atual[0] - 1 ][play[i].p_atual[1] + 1 ];
		play[i].vizinhos[5][1] = play[i].p_atual[0] -1; 
		play[i].vizinhos[5][2] = play[i].p_atual[1] +1; 
	}else{
		play[i].vizinhos[5][0] = 9;
		// validos[play[i].vizinhos[5][1]][play[i].vizinhos[5][2]] = 0;
	}

	if(play[i].p_atual[0] - 0  >= 0 && play[i].p_atual[1] + 1  >= 0 && play[i].p_atual[0] - 0  < camp && play[i].p_atual[1] + 1  < camp ){
		play[i].vizinhos[6][0] = mapa[play[i].p_atual[0] - 0 ][play[i].p_atual[1] + 1 ];
		play[i].vizinhos[6][1] = play[i].p_atual[0]; 
		play[i].vizinhos[6][2] = play[i].p_atual[1] +1;
	}else{
		play[i].vizinhos[6][0] = 9;
		// validos[play[i].vizinhos[6][1]][play[i].vizinhos[6][2]] = 0;
	}

	if(play[i].p_atual[0] + 1 >= 0 && play[i].p_atual[1] + 1 >= 0 && play[i].p_atual[0] + 1 < camp && play[i].p_atual[1] + 1 < camp){
		play[i].vizinhos[7][0] = mapa[play[i].p_atual[0] + 1 ][play[i].p_atual[1] + 1 ];
		play[i].vizinhos[7][1] = play[i].p_atual[0] +1; 
		play[i].vizinhos[7][2] = play[i].p_atual[1] +1; 
	}else{
		play[i].vizinhos[7][0] = 9;
		// validos[play[i].vizinhos[7][1]][play[i].vizinhos[7][2]] = 0;
	}

	return play[i].vizinhos;
}


int caminho_percorrido(Jogador *play, int player, int i){

    return play[player].vet_caminho[i];
}
