#include <stdio.h>
#include <stdlib.h>
#include "lista.h"
int tam;

void inicia(lstFollow *LISTA)
{
    LISTA->prox = NULL;
}

int vazia(lstFollow *LISTA)
{
    if(LISTA->prox == NULL)
        return 1;
    else
        return 0;
}

lstFollow *aloca()
{
    lstFollow *novo=(lstFollow *) malloc(sizeof(lstFollow));
    if(!novo){
        printf("Sem memoria disponivel!\n");
        exit(1);
    }
    return novo;
}


void insereFim(lstFollow *LISTA)
{
    lstFollow *novo=aloca();
    novo->prox = NULL;
	
    if(vazia(LISTA))
        LISTA->prox=novo;
    else{
        lstFollow *tmp = LISTA->prox;
		
        while(tmp->prox != NULL)
            tmp = tmp->prox;
		
        tmp->prox = novo;
    }
    tam++;
}

void insereInicio(lstFollow *LISTA)
{
    lstFollow *novo=aloca();
    lstFollow *oldHead = LISTA->prox;
	
    LISTA->prox = novo;
    novo->prox = oldHead;
	
    tam++;
}

void exibe(lstFollow *LISTA)
{
    system("clear");
    if(vazia(LISTA)){
        printf("Lista vazia!\n\n");
        return ;
    }
	
    lstFollow *tmp;
    tmp = LISTA->prox;
//	printf("Lista:");
    while( tmp != NULL){
        printf("%5d", tmp->id);
        tmp = tmp->prox;
    }
    printf("\n\n");
}

void libera(lstFollow *LISTA)
{
    if(!vazia(LISTA)){
        lstFollow *proxlstFollow,
              *atual;
		
        atual = LISTA->prox;
        while(atual != NULL){
            proxlstFollow = atual->prox;
            free(atual);
            atual = proxlstFollow;
        }
    }
}

lstFollow *retiraInicio(lstFollow *LISTA)
{
    if(LISTA->prox == NULL){
        printf("Lista ja esta vazia\n");
        return NULL;
    }else{
        lstFollow *tmp = LISTA->prox;
        LISTA->prox = tmp->prox;
        tam--;
        return tmp;
    }
				
}

lstFollow *retiraFim(lstFollow *LISTA)
{
    if(LISTA->prox == NULL){
        printf("Lista ja vazia\n\n");
        return NULL;
    }else{
        lstFollow *ultimo = LISTA->prox,
             *penultimo = LISTA;
			 
        while(ultimo->prox != NULL){
            penultimo = ultimo;
            ultimo = ultimo->prox;
        }
			 
        penultimo->prox = NULL;
        tam--;
        return ultimo;
    }
}

lstFollow *retira(lstFollow *LISTA)
{
    int opt,
        count;
    printf("Que posicao, [de 1 ate %d] voce deseja retirar: ", tam);
	
    scanf("%d", &opt);
	
    if(opt>0 && opt <= tam){
        if(opt==1)
            return retiraInicio(LISTA);
        else{
            lstFollow *atual = LISTA->prox,
                 *anterior=LISTA;
				 
            for(count=1 ; count < opt ; count++){
                anterior=atual;
                atual=atual->prox;
            }
			
        anterior->prox=atual->prox;
        tam--;
        return atual;
        }
			
    }else{
        printf("Elemento invalido\n\n");
        return NULL;
    }
}
