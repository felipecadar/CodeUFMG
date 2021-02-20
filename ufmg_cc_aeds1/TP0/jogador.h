#include <stdio.h>
#include <stdlib.h>

typedef struct 
{
    char nome[30] ;
    int *vet_caminho;  //alocar dinamicamente para 3N
	int p_inicial[2];
	int p_atual[2];
	char char_init[4];
	int score;
	int **vizinhos;
	int pokebolas;
    int jogadas;
} Jogador;

int andar(int vet[], int player, Jogador *play, int **validos);
int semPokestop(int vet[], int player, Jogador *play, int **validos);
int pokestop(int vet[], int player, Jogador *play, int **validos);
int **explorar(Jogador *play, int  i,int  camp,int  **mapa);
int caminho_percorrido(Jogador *play, int player, int i);
