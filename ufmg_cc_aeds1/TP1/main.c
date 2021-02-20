#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "lista.h"
#define lineMax 1024

char* concat(const char *s1, const char *s2)
{
    char *result = malloc(strlen(s1)+strlen(s2)+1);//+1 for the zero-terminator
    //in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}


int main(int argc, char const *argv[])
{
    int i, j, k = 0, time = 0, command, mate, message_id, usr1, usr2;  // mate -> posted a tweet, usr1 and usr2 -> 1 follow 2, message_id -> this
    user *someone;                                                     // pointer of users
    lstFollow *tmp;                                                    // FollowList pointer for manipulation
    timeLine *tmp_tl;
    char *value, linha[1024], *token, *last;
    int n_users = 0; /* number of users */
    char message[140];                                                 //tweet text

    FILE *saida;

	FILE *entrada;
    const char *url = argv[1];

    last = token = strtok(url, "/");
    for (;(token = strtok(NULL, "/")) != NULL; last = token);
//    printf("%s\n", last);

    char *url_saida = concat("log.", last);

    if(argv[1] == NULL ){
		printf("Definir arquivo de entrada como parametro\n");
		return 1;
    }

    entrada = fopen(url	, "r");

	if(entrada == NULL){
        printf("Não foi possivel abrir o arquivo \n");
		return 1;
	}

    saida = fopen(url_saida, "w");

    if(saida == NULL){
        printf("Não foi possivel abrir o arquivo \n");
        return 1;
    }

    fscanf(entrada, "%i\n", &n_users);

    someone = (user *)malloc(n_users * sizeof(user));

    for(i = 0; i < n_users; i++){
        someone[i] = scanFile(entrada);
    }

    while(fgets(linha, 1024 , entrada) != NULL ){

        k = n_partes(linha);                    // numero de ";"
        value = strtok(linha,";");
        time = atoi(value);                     //tempo
        value = strtok(NULL, ";");
        if(value == 0x0){
            return 0;
        }
        command = atoi(value);                  //comando

        switch (command) {
        case 1:

            value = strtok(NULL, ";");
            mate = atoi(value);                 //user id
            value = strtok(NULL, ";");
            message_id = atoi(value);           //message id
            value = strtok(NULL, "\n");
            strcpy(message, value);                              //message = value;

            postarMensagem(message_id, mate, time, message, someone, n_users);

            break;
        case 2:

            value = strtok(NULL,";");
            usr1 = atoi(value);

            value = strtok(NULL,"\n");
            usr2 = atoi(value);

            iniciarAmizade(someone, usr1, usr2, n_users);
            break;
        case 3:

            value = strtok(NULL,";");
            usr1 = atoi(value);

            value = strtok(NULL,"\n");
            usr2 = atoi(value);


            cancelarAmizade(someone, usr1, usr2, n_users);
            break;
        case 4:

            value = strtok(NULL,";");
            mate = atoi(value);

            value = strtok(NULL,"\n");
            message_id = atoi(value);

            someone = curtirMensagem(someone, mate, message_id, n_users);

            break;
        case 5:

            value = strtok(NULL,"\n");
            mate = atoi(value);

            exibirTimeline(someone, mate, n_users, saida);

            break;

        default:

            printf("Erro: Opção %i é invalida", command);

            break;
        }
    }

    fclose(entrada);

    return 0;
}
