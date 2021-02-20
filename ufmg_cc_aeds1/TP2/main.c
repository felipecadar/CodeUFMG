#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "times.h"
#define MAX 1024

#define QUICK 1
#define SHELL 2

int main(int argc, char const *argv[])
{
    FILE *entrada, *saida;

    team *times;

    int dia, mes, ano;      // variaveis para pesquisa no final do arquivo de entrada

    int i = 0, j = 0, k = 0;

    int sort = 0;
    int hash_size = 0;
    char line[MAX];
    char *value, data[MAX];

    long long int search_key = 0;
    int search_index = 0;

    int t_number = 0;
    int rounds = 0;
    int games_p_rounds = 0;

//    hashTable **hashArray;

    //    hashTable *aux =(hashTable*)malloc(sizeof(hashTable));


    if(argc < 4){
        entrada = fopen("entrada.txt", "r");
        saida   = fopen("saida.txt", "w");

        fgets(line, 1024, entrada);
        value = strtok(line,";");
        hash_size = atoi(value);

        value = strtok(NULL,"\n");
        sort = atoi(value);

//        printf("file mode\n");
//        printf("entrada.txt saida.txt %i %i\n",hash_size, sort);

    }else{
//        printf("Args mode\n");
//        printf("%s %s %i %i\n", argv[1], argv[2], atoi(argv[3]), atoi(argv[4]));

        entrada = fopen(argv[1], "r");
        saida   = fopen(argv[2], "w");

        hash_size = atoi(argv[3]);
        sort = atoi(argv[4]);

        fgets(line, 1024, entrada);         //jump a line

    }


    fgets(line, 1024, entrada);
    value = strtok(line,";");
    t_number = atoi(value);             //numero de times

    value = strtok(NULL,";");
    rounds = atoi(value);                   //numero de rodadas

    value = strtok(NULL,"\n");
    games_p_rounds = atoi(value);           //numero de jogos por rodadas


    hashTable **hashArray = (hashTable**)malloc(sizeof(hashTable*)*hash_size);      //malloc the hash table
//    printf("%lu\n", (long unsigned int)sizeof(**hashArray)/sizeof(*hashArray[0]));
     for(i = 0; i < hash_size; i++){
        hashArray[i] = (hashTable*)malloc(sizeof(hashTable));                   //malloc each position
    }

    times = (team*)malloc(sizeof(team)*t_number);          // malloc vetor com informações dos times

    for(i = 0; i < t_number; i++){
        fgets(line, 1024, entrada);
        value = strtok(line,"\n");
        strcpy(times[i].name,value);                    //nome de cada time
        times[i].id = i;                                //id para facilitar as operações
    }

    for(i = 0; i < t_number; i++){                      //INITIALIZE THE TEAM TABLE
        times[i].vit = 0;
        times[i].score = 0;
        times[i].sg = 0;
        times[i].gp = 0;

    }


    for(i=0; i<hash_size;i++){
        hashArray[i]->key = -1;                         //initialize the hash table with -1 keys
    }

    for(i = 0; i < rounds; i++){
        ler_rodada(entrada, games_p_rounds, hash_size, hashArray, times, t_number);     //le cada rodada

        if(sort == QUICK){
            //usar quick
            quicksort_alt(times, 0, t_number-1);                    //ordena tabela de times
        }else{
            //usar shell

            shell_sort(times, t_number);
        }

        //print tabela ordenada a cada rodada
        fprintf(saida, "%i\n", i+1);
        for(k = t_number-1; k >= 0; k--){
            fprintf(saida, "%s %i %i %i %i\n", times[k].name, times[k].score, times[k].vit, times[k].sg, times[k].gp );
        }



    }

    while (fgets(line, sizeof(line), entrada) != NULL) {

        value = strtok(line, "/");
        dia = atoi(value);
        value = strtok(NULL, "/");
        mes = atoi(value);
        value = strtok(NULL, "/");
        ano = atoi(value);

        search_key = (dia + (mes*30) + (ano*12*30));

        search_index = search_key%hash_size;

        buscarArvore(hashArray[search_index]->raiz, search_key, saida);   //busca na posição da hash_key selecionada
    }

    for(i = 0; i < hash_size; i++){
      free(hashArray[i]);                   //free HASH table
    }

    free(times);                   //free TEAM table

    return 0;
}
