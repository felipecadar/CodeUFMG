#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "times.h"

int alf(char *str1, char *str2){            //selecionar por ordem alfabética
    int i = 0;
    int param = 0;
    int t1, t2;

    t1 =strlen(str1);
    t2 =strlen(str2);

    if(t1>t2){
        param = t2;
    }else{
        param = t1;
    }

    for (i = 0; i < param; ++i)             //compara cada caracter da menor palavra
    {
        if(str1[i] > str2[i]){
            // printf("%s\n", str2);
            return 2;
        }
        if(str1[i] < str2[i]){
            // printf("%s\n", str1);
            return 1;
        }
    }

}

void ler_rodada(FILE *f, int rounds, int SIZE, hashTable *hashArray[], team times[], int t_number){
    char line[1024];
    char other_line[1024];
    char *value, *date;
    int rodada = 0, i = 0, k;
    long long int hashKey = 0;
    jogo *data;

    data = (jogo*)malloc(sizeof(jogo));

    data->chave = 0;

    fgets(line, sizeof(line), f);
    value = strtok(line," ");
    value = strtok(NULL,"\n");
    rodada = atoi(value);

//    printf("Rodada : %i\n", rodada);

    for(i = 0; i < rounds; i++){            //le cada partida da rodada
        fgets(line, sizeof(line), f);
        strcpy(other_line, line);

        value = strtok(line, ";");
        strcpy(data->data, value);

        date = strtok(value, "/");
        hashKey = atoi(date);
        date = strtok(NULL, "/");
        hashKey = hashKey + (atoi(date) * 30);
        date = strtok(NULL, "/");
        hashKey = hashKey + (atoi(date)*30*12);         //number of days since 0/0/0

        data->chave = hashKey;              //seta informações

        value = strtok(other_line, ";");
        value = strtok(NULL, ";");
        strcpy(data->team1, value);
        value = strtok(NULL, ";");
        data->team1_g = atoi(value);
        value = strtok(NULL, ";");
        strcpy(data->team2, value);
        value = strtok(NULL, ";");
        data->team2_g = atoi(value);

//        printf("Rodada:%i chave = %lli\n", i,hashKey);
        //        somar pontuações

        //        time 1
        for(k = 0; k < t_number; k++){                              //determina pontuações da "tabela do brasileirão"
            if(strcmp(data->team1, times[k].name) == 0){
                times[k].sg = data->team1_g - data->team2_g + times[k].sg;
                times[k].gp = data->team1_g + times[k].gp;

                if(data->team1_g > data->team2_g){                //vitoria
                    times[k].vit++;
                    times[k].score = times[k].score + 3;
                }else{
                    if(data->team1_g == data->team2_g){            //empate
                        times[k].score = times[k].score + 1;
                    }
                }
            }
        }

        //time 2
        for(k = 0; k < t_number; k++){
            if(strcmp(data->team2, times[k].name) == 0){
                times[k].sg = data->team2_g - data->team1_g + times[k].sg;
                times[k].gp = data->team2_g + times[k].gp;

                if(data->team2_g > data->team1_g){                    //vitoria
                    times[k].vit++;
                    times[k].score = times[k].score + 3;
                }else{
                    if(data->team2_g == data->team1_g){                //empate
                        times[k].score = times[k].score + 1;
                    }
                }
            }
        }


        insert(hashKey, *data, SIZE, hashArray);   //insere o jogo

    }

}

//void quick_sort(team *a, int left, int right){                    //possui algum erro, verificar após a data de entrega do tp
//    int i, j;

//    team x, y;

//    i = left;
//    j = right;
//    x = a[(left + right) / 2];

//    while(i <= j) {
//        if(a[i].score != x.score){
//            printf("SCORE %s %i %s %i\n",a[i].name, a[i].score, x.name, x.score);
//            while(a[i].score < x.score && i < right) {
//                i++;
//            }
//        }else{
//            if(a[i].vit != x.vit){
//                printf("VITORIAS  %s %i %s %i\n", a[i].name, a[i].vit, x.name,x.vit);
//                while(a[i].vit < x.vit && i < right) {
//                    i++;
//                }
//            }else{
//                if(a[i].sg != x.sg){
//                    printf("SG  %s %i %s %i\n",a[i].name, a[i].sg, x.name, x.sg);
//                    while(a[i].sg < x.sg && i < right) {
//                        i++;
//                    }
//                }else{
//                    if(a[i].gp != x.gp){
//                        printf("GP %s %i %s %i\n",a[i].name, a[i].gp,x.name, x.gp);
//                        while(a[i].gp < x.gp && i < right) {
//                            i++;
//                        }
//                    }else{
//                        printf("names  %s %s\n", a[i].name,x.name);
//                        while(alf(x.name, a[i].name) == 1 && i < right) {
//                            i++;

//                        }
//                    }
//                }
//            }
//        }


//        if(a[j].score != x.score){
//            printf("SCORE %s %i %s %i\n",a[j].name, a[j].score, x.name, x.score);
//            while(a[j].score > x.score && j > left) {
//                j--;
//            }
//        }else{
//            if(a[j].vit != x.vit){
//                printf("VITORIAS  %s %i %s %i\n", a[j].name, a[j].vit, x.name,x.vit);
//                while(a[j].vit > x.vit && j > left) {
//                    j--;
//                }
//            }else{
//                if(a[j].sg != x.sg){
//                    printf("SG  %s %i %s %i\n",a[j].name, a[j].sg, x.name, x.sg);
//                    while(a[j].sg > x.sg && j > left) {
//                        j--;
//                    }
//                }else{
//                    if(a[j].gp != x.gp){
//                        printf("GP %s %i %s %i\n",a[j].name, a[j].gp,x.name, x.gp);
//                        while(a[j].gp > x.gp && j > left) {
//                            j--;

//                        }
//                    }else{
//                        printf("names: %s %s \n", a[j].name, x.name);
//                        while (alf(x.name, a[j].name) == 2 && j >left) {
//                            j--;
//                        }
//                    }
//                }
//            }
//        }
//        if(i <= j) {
//            y = a[i];
//            a[i] = a[j];
//            a[j] = y;
//            i++;
//            j--;
//        }
//    }

//    if(j > left) {
//        quick_sort(a, left, j);
//    }
//    if(i < right) {
//        quick_sort(a, i, right);
//    }
//}

void shell_sort(team *a, int size){                         //perfeito
    int i , j;

    team value;
    int gap = 1;

    do {
        gap = 3*gap+1;
    } while(gap < size);

    do {
        gap /= 3;
        for(i = gap; i < size; i++) {
            value = a[i];
            j = i - gap;
            if(value.score != a[j].score){
                while (j >= 0 && value.score < a[j].score) {
                    a[j + gap] = a[j];
                    j -= gap;
                }
            }else{
                if(value.vit != a[j].vit){
                    while (j >= 0 && value.vit < a[j].vit) {
                        a[j + gap] = a[j];
                        j -= gap;
                    }
                }else{
                    if(value.sg != a[j].sg){
                        while (j >= 0 && value.sg < a[j].sg) {
                            a[j + gap] = a[j];
                            j -= gap;
                        }
                    }else{
                        if(value.gp != a[j].gp){
                            while (j >= 0 && value.gp < a[j].gp) {
                                a[j + gap] = a[j];
                                j -= gap;
                            }
                        }else{

                            while (j >= 0 && alf(value.name, a[j].name) == 1) {
                                a[j + gap] = a[j];
                                j -= gap;
                            }
                        }
                    }
                }
            }


            a[j + gap] = value;
        }
    }while(gap > 1);
}




// -------------------------- QUICKSORT RECURSIVO ALTERNATIVO FUNCIONAL-----------------------//

void quicksort_alt(team v[], int esq, int dir)
{
    int i;
    if(esq >= dir){
        return;
    }
    i = particao(v, esq, dir);
    quicksort_alt(v,esq,i-1);
    quicksort_alt(v,i+1,dir);

}
int particao(team v[], int esq, int dir){
    int i, fim;
    void troca(team v[],int i,int j);
    troca(v, esq, (esq+dir)/2);
    fim = esq;
    for(i = esq+1; i <= dir; i++){
        if(v[i].score != v[esq].score){
            if(v[i].score < v[esq].score){
                troca(v, ++fim, i);
            }
        }else {
            if(v[i].vit != v[esq].vit){
                if(v[i].vit < v[esq].vit){
                    troca(v, ++fim, i);
                }
            }else {
                if(v[i].sg != v[esq].sg){
                    if(v[i].sg < v[esq].sg){
                        troca(v, ++fim, i);
                    }
                }else{
                    if(v[i].gp != v[esq].gp){
                        if(v[i].gp < v[esq].gp){
                            troca(v, ++fim, i);
                        }
                    }else{
                        if(alf(v[i].name, v[esq].name) == 2){
                            troca(v, ++fim, i);
                        }
                    }
                }

            }
        }
    }
    troca(v, esq, fim);
    return fim;
}

void troca(team v[], int i,int j){
    team temp;
    //    temp = (team*)malloc(sizeof(team));
    temp=v[i];
    v[i]=v[j];
    v[j]=temp;
}
