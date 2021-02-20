#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "lista.h"
void iniciarAmizade(user someone[], int user1, int user2, int n_users){
    int i, j;
    lstFollow *tmp;
    for(i = 0; i < n_users; i++){
        if(user1 == someone[i].id){
            tmp = someone[i].follow;
            insereFollow(someone[i].follow, user2);

//            printf("User %i followed %i\n", user1, user2);
        }
        if(user2 == someone[i].id){
            tmp = someone[i].follow;
            insereFollow(someone[i].follow, user1);

            tmp->id = user2;
//            printf("User %i followed %i\n", user2, user1);
        }
    }
    free(tmp);
}

void cancelarAmizade(user someone[], int user1, int user2, int n_users){
    int i, j;
    lstFollow *tmp;
    lstFollow *proxTmp;
    for(i = 0; i < n_users; i++){
        if(user1 == someone[i].id){
            tmp = someone[i].follow;
            proxTmp = someone[i].follow->prox;
            while (proxTmp->id != user2) {
                tmp = tmp->prox;
                proxTmp = proxTmp->prox;
            }
            tmp->prox = proxTmp->prox;

//            printf("User %i unfollowed %i\n", user1, user2);
        }
        if(user2 == someone[i].id){
            tmp = someone[i].follow;
            proxTmp = someone[i].follow->prox;
            while (proxTmp->id != user1) {
                tmp = tmp->prox;
                proxTmp = proxTmp->prox;
            }
            tmp->prox = proxTmp->prox;


//            printf("User %i unfollowed %i\n", user2, user1);
        }

    }
    free(tmp);
    free(proxTmp);
}
void verAmigos(){

}



lstFollow *alocaFollow(){
    lstFollow *novo=(lstFollow *)malloc(sizeof(lstFollow));
    if(!novo){
        printf("Sem memoria disponivel!\n");
        exit(1);
    }
}


int followSomeone(int id, lstFollow *follow){
    lstFollow *tmp= follow;

    //verifica se someone[i] é amigo de quem postou a mensagem

    if(id == tmp->id){
        return 1;
    }

    while(tmp->prox != NULL){
        tmp = tmp->prox;
        if(id == tmp->id){
            return 1;
        }
    }
    tmp = NULL;
    free(tmp);
}

void insereFollow(lstFollow *LISTA, int id){
    lstFollow *novo=alocaFollow();
    lstFollow *tmp;
    novo->id = id;
    novo->prox = NULL;

    if(vazia(LISTA))
        LISTA->prox=novo;
    else{
        tmp = LISTA->prox;

        while(tmp->prox != NULL)
            tmp = tmp->prox;

        tmp->prox = novo;
    }
}

int n_partes(char *line){
    int i = 0, n=0;
    char c;

    while(c != '\n'){
        c = line[i];

        if(c == ';'){
            n++;
        }

        i++;
    }
    return n;
}

void exibeFollow(lstFollow *LISTA){
    if(vazia(LISTA)){
        printf("Lista vazia!\n\n");
        return ;
    }

    lstFollow *tmp;
    tmp = LISTA->prox;
//	printf("Lista:");
    while( tmp != NULL){
        printf("%i", tmp->id);
        tmp = tmp->prox;
    }
    printf("\n\n");
}
user scanFile(FILE* info){
    char line[1024];
    char *value;
    int i = 0, j, lstCont = 1, k = 0;
    int tmpInt;
    user someone;
    lstFollow *tmp;

    someone.follow = (lstFollow*)malloc(sizeof(lstFollow));
    someone.follow->prox = NULL;

    //fgets(line, sizeof(line), info);
    fgets(line, 1024, info);
    if(line[0] == '\n'){
        fgets(line, sizeof(line), info);
    }

    j = n_partes(line);

    value = strtok(line,";");

    someone.id = atoi(value);
//    printf("scanFile: %i\n",someone->id);

    value = strtok(NULL, ";");
    //someone.name = value;
    strcpy(someone.name, value);
//    printf("scanFile: %s\n",someone->name);


//    someone.follow->prox = NULL;

    if(j == 1){return someone;}         //someone don't have friends :(

    for(i = 0; i < j-2; i++){

        value = strtok(NULL, ";");
        tmpInt = atoi(value);

        insereFollow(someone.follow, tmpInt);
    }

    value = strtok(NULL, "\n");
    tmpInt = atoi(value);

    insereFollow(someone.follow, tmpInt);

    someone.tl.prox=NULL;

    return someone;
}

void postarMensagem(int message_id, int user_id, int time, char message[140], user someone[], int n_user){
    int i;


    for(i = 0; i < n_user; i++){


        if(followSomeone(user_id, someone[i].follow) == 1 | user_id == someone[i].id){
//            printf("insere");
            //  adicioar post na tl
            insereTweet(someone[i].id,message_id, time, message, &someone[i].tl);


        }


    }

}



void exibirTimeline(user someone[], int mate,int n_users, FILE *saida){
    int i, j;
    timeLine *tmp_tl;

//    for(i = 0; i < n_users; i++){
//        if(someone[i].id == mate){
//            printf("%i %s\n", mate, someone[i].name);
//        }
//    }


//    for(i = 0; i < n_users; i++){                                                 //termial print
//        if(someone[i].id ==  mate ){

//            tmp_tl = someone[i].tl.prox;
//            while(tmp_tl->prox != NULL){
//                tmp_tl = tmp_tl->prox;
//            }

//            printf("%i %s %i\n",tmp_tl->post.id, tmp_tl->post.post, tmp_tl->post.favs );
//            imprime_rev_lista(*someone[i].tl.prox);

//        }
//     }

    for(i = 0; i < n_users; i++){
        if(someone[i].id == mate){

            fprintf(saida,"%i %s\n", mate, someone[i].name);
        }
    }


    for(i = 0; i < n_users; i++){                                                 //termial print
        if(someone[i].id ==  mate ){

            tmp_tl = someone[i].tl.prox;
            while(tmp_tl->prox != NULL){
                tmp_tl = tmp_tl->prox;
            }

            fprintf(saida,"%i %s %i\n",tmp_tl->post.id, tmp_tl->post.post, tmp_tl->post.favs );
            imprime_rev_lista(*someone[i].tl.prox, saida);

        }
     }







}

user *curtirMensagem(user someone[], int mate, int message_id,int n_users){

    int i, j, stop = 0;
    timeLine *tmp, *fn, *aux;

    for(i = 0; i < n_users; i++){
        fn = someone[i].tl.prox;
        while(fn->prox != NULL){
            fn = fn->prox;              //final da lista
        }


        stop = 0;
        aux = &someone[i].tl;
        tmp = someone[i].tl.prox;
        while (tmp->prox != NULL && stop == 0) {
            if(tmp->post.id == message_id){

                tmp->post.favs++;

                fn->prox = aux->prox;
                aux->prox = tmp->prox;
                tmp->prox = NULL;


                stop = 1;

            }
            if(stop != 1){
                aux = aux->prox;
                tmp = tmp->prox;
            }
        }

    }
    return someone;
}

//timeLine* inverte_lista(timeLine **tl){
//    timeLine *pa, *p, *pd;

//    if(*tl != NULL){
//        pa = NULL;
//        p = *tl;
//        pd = p->prox;
//        do{
//            p->prox = pa;
//            pa = p;
//            p = pd;
//            if(pd != NULL){
//                pd = pd->prox;
//            }
//        }while(p != NULL);
//        *tl = pa;
//    }
//}


void imprime_rev_lista(timeLine tl, FILE *saida){
    if(tl.prox == NULL) {
        return;
    }
    imprime_rev_lista(*tl.prox, saida);
    fprintf(saida,"%i %s %i\n",tl.post.id, &tl.post.post, tl.post.favs );
}






