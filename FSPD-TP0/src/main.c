#include <limits.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

#include "barreira.h"
#include "thread_btree.h"

#define MAX 5
#define NUM_THREADS 10

TBarreira bar;

typedef struct threadArgs {
    TipoApontador *root;
    int tid;
    int init_val;
} threadArgs;

double randBetween(double min, double max) {
    return ((double)rand() / RAND_MAX) * (max - min) + min;
}

void *test_thread(void *void_args) {
    // Get args
    threadArgs *args = (threadArgs *)void_args;
    printf("Thread %i - [start:%i]\n", args->tid, args->init_val);
    
    // Gen Insert Vector
    TipoChave *vetor = malloc(MAX * sizeof(TipoChave));
    for(long i=0; i < MAX; i++){
        vetor[i] = i + (args->init_val);
    }
    printf("Thread %i - Permut vetor\n", args->tid);
    Permut(vetor, MAX-1);

    for(long i=0; i < MAX; i++){
        printf("Thread %i - %li\n", args->tid, vetor[i]);
    }

    barreira(&bar);

    printf("Thread %i - Insert All\n", args->tid);
    // Insert in btree
    TipoRegistro X;

    // printf("Root addr: %p - %p\n", args->root, &(args->root));

    for(int i=0; i < MAX; i++){
        X.Chave = vetor[i];
        Insere(X, args->root);
    }

    barreira(&bar);
    // Testa(root);

    // if (args->tid == 0){
    //     Central(*(args->root));
    //     CentralSem(*(args->root));
    // }

    // Retira uma chave aleatoriamente e realiza varias pesquisas
    printf("Thread %i - Random Remove and Search\n", args->tid);
    for (int i = 0; i <= MAX; i++) {
        int k = i; //(int)(MAX * rand() / (RAND_MAX + 1.0));
        long n = vetor[k];
        X.Chave = n;
        printf("Thread %i Retirando chave: %ld\n", args->tid ,X.Chave);
        Retira(X, args->root);
        printf("Thread %i Retirou chave: %ld\n", args->tid ,X.Chave);
        CentralSem(*(args->root));

        for (int j = 0; j < MAX; j++) {
            X.Chave = vetor[j];//vetor[(int)(MAX * rand() / (RAND_MAX + 1.0))];
            if (X.Chave != n) {
                printf("Thread %i Pesquisando chave: %ld\n", args->tid, X.Chave);
                Pesquisa(&X, args->root);
            }
        }
        X.Chave = n;
        Insere(X, args->root);
        printf("Thread %i - Inseriu chave: %ld\n", args->tid ,X.Chave);
        CentralSem(*(args->root));
    }
    barreira(&bar);
    Testa(*(args->root));

    // Retira a raiz da arvore ate que ela fique vazia
    printf("Thread %i - Remove All\n", args->tid);
    for (int i = 0; i < MAX; i++) {
        X.Chave = vetor[i];
        printf("Thread %i Retirando chave: %ld\n", args->tid ,X.Chave);
        Retira(X, args->root);
        printf("Thread %i Retirou chave: %ld\n", args->tid ,X.Chave);
        CentralSem(*(args->root));
    }
    barreira(&bar);

    Testa(*(args->root)); 
    printf("[Exit] Thread %i\n", args->tid);
    pthread_exit(NULL);
}

int main() {
    int i;


    // Creating Tree
    TipoNo *btree;
    Inicializa(&btree);

    // Creating args
    threadArgs args[NUM_THREADS];
    for (i = 0; i < NUM_THREADS; i++) {
        args[i].init_val = i*MAX;
        args[i].tid = i;
        args[i].root = &btree;
    }

    printf("Root addr: %p - %p\n", btree, &btree);
    // Creating Threads
    init_barreira(&bar, NUM_THREADS);

    pthread_t threads[NUM_THREADS];
    for (i = 0; i < NUM_THREADS; i++) {

        printf("Root addr: %p - %p\n", args[i].root, &args[i].root);
        

        int rc = pthread_create(&threads[i], NULL, test_thread, (void *)&args[i]);
        if (rc) {
            printf("ERROR; return code from pthread_create() is %d\n", rc);
            exit(-1);
        }
    }

    // Join Threads
    for (i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    return 0;
}