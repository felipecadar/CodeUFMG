#include <stdlib.h>
#include <stdio.h>
#include "mensagem.h"


int tl_vazia(timeLine *tl){
    if(tl->prox == NULL){
        return 1;
    }else{
        return 0;
    }
}

timeLine *alocaTl(){
    timeLine *novo=(timeLine *)malloc(sizeof(timeLine));
    novo->prox = NULL;
    if(!novo){
        printf("Sem memoria disponivel!\n");
        exit(1);
    }
}

void insereTweet(int owner, int id, int time, char post[140], timeLine *tl){
    timeLine *novo = alocaTl();
    timeLine *tmp;

    novo->post.id= id;
    novo->post.time = time;
    strcpy(novo->post.post, post);
    novo->prox = NULL;
    novo->post.owner = owner;


     if(tl_vazia(tl) == 1){
        tl->prox = novo;
    }else{
         tmp = tl->prox;
        while(tmp->prox != NULL){
            tmp = tmp->prox;
        }
        tmp->prox = novo;

    }
}






