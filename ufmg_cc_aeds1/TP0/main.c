#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "jogador.h"

int camp; // tamanho do campo 

int **validos; 




int main(int argc, char *argv[ ] )
{
	bool playing = true;

    char *url;
    url = argv[1];

    int i, j, v, h, p;       		//contadores;

    int **mapa; 			// mapa do jogo;r

    Jogador *play;

	int n_play = 0;			// zero por defalt;

    FILE *entrada;
    FILE *saida;

	int ao_redor[8];

	int rodada = 0;

	int r_max = 0;

	int agr = 0, max_score;

    int p_max_score = 0, n_max;

    int *ganhadores, p_empates, j_empates, cont_desempate, p_desempate;


	entrada = fopen(url, "r");
    if(entrada == NULL){
        printf("Erro: não foi possivel abrir o arquivo entrada\n");
		return 1;
	}

    saida = fopen("saida.txt", "w");
    if(saida == NULL){
        printf("Erro: não foi possivel abrir o arquivo saida\n");
        return 1;
    }



    fscanf(entrada,"%i", &camp);			// tamanho do campo

    r_max = 3*camp;

//    printf("%i\n", camp);  //confere o tamanho do campo;
    

    mapa = calloc(camp,  sizeof(int *));             //aloca a matriz que contem as informações do campo
		for(i=0; i < camp; ++ i){
            mapa[i] = calloc(camp, sizeof(int));
		}


    validos = (int **)malloc (camp * sizeof(int *));             //aloca a matriz que contem as informações do campo 
		for(i=0; i < camp; ++ i){
			validos[i] = (int *)malloc(camp*sizeof(int));	
		}

	if(validos == NULL){
        printf("validos nao alocado \n");
		return 1;
	}

	for (j = 0; j < camp; ++j)
	{
		for (i = 0; i < camp; ++i)
		{
            fscanf(entrada, "%i", &mapa[j][i]);
		}
	}


//	for (j = 0; j < camp; ++j)
//	{
//		for (i = 0; i < camp; ++i)
//		{
//			printf("%i ", mapa[j][i]);
//		}
//		printf("\n");
//	}

	fscanf(entrada, "%i", &n_play);     //numero de jogadores

	// printf("malloc 1 \n");    
    play = (Jogador *)malloc (n_play * sizeof(Jogador));  // cria n jogadores

    for (i = 0; i < n_play; ++i)
    {
 		play[i].vet_caminho = (int *)malloc(camp * 6 * sizeof(int));
    }



    if (play == NULL || play == 0)
    {
//    	printf("nao alocado \n");
    	return 1;
    }

    for(j = 0; j < n_play; j++){	
	    play[j].vizinhos = (int **)malloc (8 * sizeof(int *));             //aloca a matriz que contem as informações do campo 
		for(i=0; i < 8; ++ i){
			play[j].vizinhos[i] = (int *)malloc(3 * sizeof(int));	
		}
    }



   /*
    *	Scaneia os nomes e caminhos iniciais
    */
    for (i = 0; i < n_play; ++i)
    {
    	fscanf(entrada, "%s", play[i].nome);
    	// printf("%s\n", play[i].nome);
    	fscanf(entrada, "%s", play[i].char_init);
    }

    // for (i = 0; i < n_play; ++i)
    // {
    //     printf("%s\n", play[i].nome);
    //     printf("%s\n", play[i].char_init);
    // }

    /*	
     *ajusta as posições iniciais
     */
   	for (i = 0; i < n_play; ++i)
	{
		play[i].p_inicial[0] = atoi(&play[i].char_init[0]);
		play[i].p_inicial[1] = atoi(&play[i].char_init[2]);

		play[i].p_atual[0] = play[i].p_inicial[0];
		play[i].p_atual[1] = play[i].p_inicial[1];

		// printf("Vetor %i : %i\n", i, play[i].p_inicial[0]);
		// printf("Vetor %i : %i\n", i, play[i].p_inicial[1]);
	}

	for (i = 0; i < n_play; ++i)
	{	
		rodada = 0;
		playing = true;
		play[i].pokebolas = 3;
        play[i].jogadas = 0;

		for (v = 0; v < camp; ++v)
		{
			for (h = 0; h < camp; ++h)
			{
				
				validos[v][h] = 1;
//				printf("%i ", validos[v][h]);
			}
//			printf("\n");
		}

		validos[play[i].p_inicial[0]][play[i].p_inicial[1]] = 0;				//primeira jogada do jogador deve ser fora do while
		play[i].score = mapa[play[i].p_inicial[0]][play[i].p_inicial[1]];				
		if(play[i].score != 0){
			play[i].pokebolas--;
		}else{

		}

		while(playing == true ){

			if(rodada > r_max){playing = false;}

//			for (v = 0; v < camp; ++v)
//		{
//					for (h = 0; h < camp; ++h)
//					{
//						printf("%i ", validos[v][h]);
//					}
//					printf("\n");
//				}
			

		play[i].vizinhos = explorar( play, i, camp, mapa);



//			for (j = 0; j < 8; ++j)
//			{
//				printf("Jogador: %i   --> Valor :%i --> (%i, %i)\n", i, play[i].vizinhos[j][0], play[i].vizinhos[j][1], play[i].vizinhos[j][2]);
//			}



			for(j = 0; j < 8; j++){
				ao_redor[j] = play[i].vizinhos[j][0];			// salva valores de forma ordenada
			}


			if(rodada >= r_max){						// é a ultima jogada  do jogador ? 
                playing = false;
			}

				if(play[i].pokebolas > 0){
                agr = andar(ao_redor, i, play, validos);


				if(agr == 404){
					playing = false;
//					printf("PAARRAA 404\n");			//impossivel continuar
					break;
				}



				play[i].score =  play[i].score + play[i].vizinhos[agr][0];
				play[i].pokebolas--;
				play[i].p_atual[0] = play[i].vizinhos[agr][1];					// atualiza score, celula atual, pokebolas, celullas validas
				play[i].p_atual[1] = play[i].vizinhos[agr][2];
				validos[play[i].p_atual[0]][play[i].p_atual[1]] = 0;
                play[i].jogadas++;

                if(play[i].vizinhos[agr][0] <= 0){
					play[i].pokebolas++;
				}

                // printf("---- maior\n");
                // printf("Jogador: %i   --> Valor :%i --> (%i, %i)\n", i, play[i].vizinhos[agr][0], play[i].vizinhos[agr][1], play[i].vizinhos[agr][2]);
                // printf("----\n");

                // printf("Poke :%i    Score: %i   P-Atual %i, %i\n", play[i].pokebolas, play[i].score, play[i].p_atual[0], play[i].p_atual[1]);


				}else{
					agr = pokestop(ao_redor, i, play, validos);

					if(agr == 90){
						agr = semPokestop(ao_redor, i, play, validos);

                        if(agr == 404 ){
                            playing = false;
                            break;
                        }

						play[i].p_atual[0] = play[i].vizinhos[agr][1];			//não possui pokestop -- > só anda
						play[i].p_atual[1] = play[i].vizinhos[agr][2];
						validos[play[i].p_atual[0]][play[i].p_atual[1]] = 0;
                        play[i].jogadas++;

                        // printf("---- Sem Pokestop\n");
                        // printf("Jogador: %i   --> Valor :%i --> (%i, %i)\n", i, play[i].vizinhos[agr][0], play[i].vizinhos[agr][1], play[i].vizinhos[agr][2]);
                        // printf("----\n");
                        // printf("Poke :%i    Score: %i   P-Atual %i, %i\n", play[i].pokebolas, play[i].score, play[i].p_atual[0], play[i].p_atual[1]);


					}else{


						play[i].pokebolas = 3;
						play[i].p_atual[0] = play[i].vizinhos[agr][1];			//entrou no pokestop
						play[i].p_atual[1] = play[i].vizinhos[agr][2];

						validos[play[i].p_atual[0]][play[i].p_atual[1]] = 0;
                        play[i].jogadas++;

                        // printf("---- Pokestop\n");
                        // printf("Jogador: %i   --> Valor :%i --> (%i, %i)\n", i, play[i].vizinhos[agr][0], play[i].vizinhos[agr][1], play[i].vizinhos[agr][2]);
                        // printf("----\n");
                        // printf("Poke :%i    Score: %i   P-Atual %i, %i\n", play[i].pokebolas, play[i].score, play[i].p_atual[0], play[i].p_atual[1]);

					}
				}


			play[i].vet_caminho[(2*rodada) -1] = play[i].p_atual[0];			//salva caminho percorrido
			play[i].vet_caminho[2*rodada] = play[i].p_atual[1];

			rodada++;
		}	
    }

    for(i = 0; i < n_play; i++){
        fprintf(saida, "%s %i ", play[i].nome, play[i].score);
        for(j = 0; j < 2*play[i].jogadas; j = j+2){
            fprintf(saida, "%i,%i ", caminho_percorrido(play, i, j), caminho_percorrido(play, i, j+1));    		//caminho percorrido
        }
        fprintf(saida, "\n");

    }

// ganhadores
    fprintf(saida, "VENCEDORES ");
    max_score = play[0].score;
    n_max = 0;

    for(i = 0; i < n_play; i++){
        if(play[i].score > max_score){
            p_max_score = i;
        }
    }

    max_score = play[p_max_score].score;

    for(i = 0; i < n_play; i++){
        if(play[i].score == max_score){
            n_max++;
        }
    }


    if(n_max == 1){
        fprintf(saida, "%s", play[p_max_score].nome);
    }else{
        p_empates = 0;
        j_empates = 0;
        cont_desempate = 0;
        p_desempate = 0;
        ganhadores = (int *)malloc(n_max * sizeof(int));

        for(i = 0; i < n_play; i++){
            if(play[i].score == max_score){
                ganhadores[p_empates] = i;
                p_empates++;				//posição de empates
            }
        }

        for(i = 0; i < p_empates; i++){
            if(play[i].jogadas > j_empates){
                   j_empates = play[i].jogadas;		//desempate por jogadas
                   p_desempate = i;			//posição do desempate
            }
        }

        for(i = 0; i < p_empates; i++){
            if(play[i].jogadas == j_empates){
                  cont_desempate++;				//contagem desempates
            }
        }


        if(cont_desempate == 1){
            fprintf(saida, "%s", play[p_desempate].nome);
        }else{
            for(i = 0; i < p_empates; i++){
                fprintf(saida, "%s ", play[i].nome);			//arquivo saida
            }

        }

    }
	


    for (i = 0; i < camp; ++i)
    {
    	free(mapa[i]);
    	free(validos[i]);
    }
    free(mapa);
    free(validos); 

    fclose(entrada);  // fecha o arquivo
    fclose(saida);

    return 0;
}


