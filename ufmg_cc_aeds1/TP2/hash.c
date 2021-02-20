#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "hash.h"

int hashCode(long long int key, int SIZE) {
    return key % SIZE;
}

hashTable *search(long long int key, int SIZE, hashTable* hashArray[]) {
    //get the hash
    int hashIndex = hashCode(key, SIZE);
    int init = hashIndex;
    //move in array until an empty
    while(hashArray[hashIndex] != NULL) {
        if(hashArray[hashIndex]->key == key){

//            printf("Found with %i colisions\n",hashArray[hashIndex]->colisoes);
        }

        ++hashIndex;

        //wrap around the table
        hashIndex %= SIZE;
        if(hashIndex == init){
            return NULL;
        }
    }

    return NULL;
}

void insert(long long int key,jogo data, int SIZE, hashTable* hashArray[]) {

    //get the index
    int hashIndex = hashCode(key, SIZE);

    if (hashIndex < 0){
        hashIndex = hashIndex * (-1);
    }

    if(hashArray[hashIndex]->key == -1){            //POSIÇÃO DISPONIVEL

        hashArray[hashIndex]->raiz = (struct sbb*)malloc(sizeof(struct sbb));

        hashArray[hashIndex]->raiz->reg = data;
        hashArray[hashIndex]->raiz->dir = NULL;
        hashArray[hashIndex]->raiz->esq = NULL;

        hashArray[hashIndex]->colisoes = 0;
//        printf("SEM COLISOES Time: %s gols: %i --- Time: %s gols: %i\n",data.team1, data.team1_g, data.team2, data.team2_g);
        hashArray[hashIndex]->key = key;
        hashArray[hashIndex]->raiz->reg.colision_key = key;
        hashArray[hashIndex]->raiz->reg.chave = key*10000;
    }else{      // resolver colisão
//        printf("COLISOES Time: %s gols: %i --- Time: %s gols: %i\n",data.team1, data.team1_g, data.team2, data.team2_g);
        hashArray[hashIndex]->colisoes++;
        data.colision_key = key;
        key = (key * 10000)+(hashArray[hashIndex]->colisoes); // OTIMIZAÇÃO DA TABELA HASH -->> CHAVE SECUNDARIA DE COLISÃO
        data.chave = key;
//        printf("%lli\n", key);
        insere(data, &(*hashArray[hashIndex]).raiz);
    }
}
