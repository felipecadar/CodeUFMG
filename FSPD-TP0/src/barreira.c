#include "barreira.h"
#include <stdlib.h>

int numThreads;
int doneThreads;
pthread_cond_t barCond;

void init_barreira(TBarreira* b, int n){
    pthread_mutex_lock(b);
    numThreads = n;
    doneThreads = 0;
    pthread_mutex_unlock(b);
}

void barreira(TBarreira *b){
    pthread_mutex_lock(b);
    doneThreads++;
    if(doneThreads == numThreads){
        doneThreads = 0;
        pthread_cond_broadcast(&barCond);
    }else{
        pthread_cond_wait(&barCond, b);
    }
    pthread_mutex_unlock(b);
}

