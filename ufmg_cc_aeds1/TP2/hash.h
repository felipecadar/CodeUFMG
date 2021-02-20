#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "tree.h"


struct hashTable {
    struct sbb *raiz;
    long long int key;
    int colisoes;
};
typedef struct hashTable hashTable;


struct hashTable* dummyItem;
struct hashTable* item;

int hashCode(long long int key, int SIZE);
hashTable *search(long long int key, int SIZE, hashTable* hashArray[]);
void insert(long long int key,jogo data, int SIZE, hashTable* hashArray[]);
