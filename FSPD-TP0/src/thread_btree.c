#include "thread_btree.h"

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

void debugSem(TipoApontador *p, char op) {
    int o;
    int r;
    int a;
    // return;
    // printf("%p\n", *p);
    if (p != NULL) {
        sem_getvalue(&((*p)->ordering), &o);
        sem_getvalue(&((*p)->rmutex), &r);
        sem_getvalue(&((*p)->area), &a);

        printf("[%c o[%i] r[%i] A[%i]] - %li\n", op, o, r, a, (*p)->Reg.Chave);
    }
    else{
        printf("[%c] NULL\n", op);
    }
    // if (op == 'C') {
    //     if (o + r + a < 3) {
    //         exit(1);
    //     }
    // }
}

void startRead(TipoApontador *p) {
    if(*p == NULL){
        printf("NULL MF\n");
        return;
    }


    sem_wait(&((*p)->ordering));  // preserves ordering
    sem_wait(&((*p)->rmutex));    // controll readcount

    (*p)->readCount++;
    if ((*p)->readCount == 1) {   // First Reader In
        sem_wait(&((*p)->area));  // controll read/write area
    }
    sem_post(&((*p)->ordering));  // next in line
    sem_post(&((*p)->rmutex));    // release readcount
    debugSem(p, 'R');
}

void endRead(TipoApontador *p) {
    if(*p == NULL){
        printf("NULL MF\n");
        return;
    }
    sem_wait(&((*p)->rmutex));  // controll readcount

    (*p)->readCount--;
    if ((*p)->readCount == 0) {   // Last Reader Out
        sem_post(&((*p)->area));  // Release read/write area
    }

    sem_post(&((*p)->rmutex));  // release readcount
    debugSem(p, 'R');
}

void startWrite(TipoApontador *p) {
    if(*p == NULL){
        printf("NULL MF\n");
        return;
    }
    debugSem(p, 'W');
    sem_wait(&((*p)->ordering));  // preserves ordering

    sem_wait(&((*p)->area));  // preserves ordering

    sem_post(&((*p)->ordering));  // preserves ordering
    printf("[W] Locked\n");
}

void endWrite(TipoApontador *p) {
    if(*p == NULL){
        printf("NULL MF\n");
        return;
    }
    sem_post(&((*p)->area));  // preserves ordering
    printf("[W] Unlock\n");
    debugSem(p, 'W');
}

void Pesquisa(TipoRegistro *x, TipoApontador *p) {
    startRead(p);
    //< CRITICAL SECTION >
    if (*p == NULL) {
        printf("Erro: Registro nao esta presente na arvore\n");
        endRead(p);
        return;
    } else {
        if (x->Chave < (*p)->Reg.Chave) {
            endRead(p);
            Pesquisa(x, &(*p)->Esq);
            return;
        }
        if (x->Chave > (*p)->Reg.Chave) {
            Pesquisa(x, &(*p)->Dir);
        } else {
            *x = (*p)->Reg;
        }
    }
    endRead(p);
    //< CRITICAL SECTION >
}

void Insere(TipoRegistro x, TipoApontador *p) {
    if (*p == NULL) {
        *p = (TipoApontador)malloc(sizeof(TipoNo));
        (*p)->Reg = x;
        (*p)->Esq = NULL;
        (*p)->Dir = NULL;

        sem_init(&((*p)->area), 0, 1);
        sem_init(&((*p)->rmutex), 0, 1);
        sem_init(&((*p)->ordering), 0, 1);
        (*p)->readCount = 0;
        return;
    }
    if (x.Chave < (*p)->Reg.Chave) {
        startRead(p);
        Insere(x, &(*p)->Esq);
        endRead(p);
        return;
    }
    if (x.Chave > (*p)->Reg.Chave) {
        startRead(p);
        Insere(x, &(*p)->Dir);
        endRead(p);
    } else {
        printf("Erro : Registro ja existe na arvore\n");
    }
}

void Inicializa(TipoApontador *Dicionario) {
    *Dicionario = NULL;
}

void Antecessor(TipoApontador q, TipoApontador *r) {
    printf("IN antecessor %li %li\n", q->Reg.Chave, (*r)->Reg.Chave);

    startRead(r);
    if ((*r)->Dir != NULL) {
        endRead(r);
        Antecessor(q, &(*r)->Dir);
        return;
    }
    endRead(r);
    startWrite(&(q));
    q->Reg = (*r)->Reg;
    endWrite(&(q));
    q = *r;
    *r = (*r)->Esq;
    free(q);
}

void Retira(TipoRegistro x, TipoApontador *p) {
    startRead(p);
    TipoApontador Aux;
    if (*p == 0x0) {
        printf("Erro : Registro nao esta na arvore\n");
        return;
    }
    printf("%d, %d, %d, %d\n",(x.Chave < (*p)->Reg.Chave),  (x.Chave > (*p)->Reg.Chave), ((*p)->Dir == NULL), ((*p)->Esq != NULL));
    if (x.Chave < (*p)->Reg.Chave) {
        endRead(p);
        Retira(x, &(*p)->Esq);
        return;
    }
    if (x.Chave > (*p)->Reg.Chave) {
        endRead(p);
        Retira(x, &(*p)->Dir);
        return;
    }

    if ((*p)->Dir == 0x0) {
        endRead(p);

        startWrite(p);
        // debugSem(p, 'C');
        // debugSem(&((*p)->Esq), 'C');
        // printf("--\n");
        Aux = *p;
        *p = (*p)->Esq;
        // debugSem(p, 'A');
        endWrite(&(Aux));
        free(Aux);
        return;
    }

    if ((*p)->Esq != 0x0) {
        endRead(p);

        startWrite(p);
        Antecessor(*p, &(*p)->Esq);
        endWrite(p);

        return;
    }

    endRead(p);

    startWrite(p);
    Aux = *p;
    *p = (*p)->Dir;

    free(Aux);
}

void Central(TipoApontador p) {
    if (p == NULL)
        return;
    Central(p->Esq);
    printf("%ld\n", p->Reg.Chave);
    Central(p->Dir);
}

void CentralSem(TipoApontador p) {
    if (p == NULL)
        return;

    debugSem(&p, 'D');

    CentralSem(p->Esq);
    CentralSem(p->Dir);
}

double rand0a1() {
    double resultado = (double)rand() / RAND_MAX; /* Dividir pelo maior inteiro */
    if (resultado > 1.0)
        resultado = 1.0;
    return resultado;
}

void Permut(TipoChave A[], int n) {
    int i, j;
    TipoChave b;
    for (i = n; i > 0; i--) {
        j = (i * rand0a1());
        b = A[i];
        A[i] = A[j];
        A[j] = b;
    }
}

void TestaI(TipoNo *p) {
    if (p == NULL) return;
    if (p->Esq != NULL) {
        if (p->Reg.Chave < p->Esq->Reg.Chave) {
            printf("Erro: Pai %ld menor que filho a esquerda %ld\n", p->Reg.Chave,
                   p->Esq->Reg.Chave);
            exit(1);
        }
    }
    if (p->Dir != NULL) {
        if (p->Reg.Chave > p->Dir->Reg.Chave) {
            printf("Erro: Pai %ld maior que filho a direita %ld\n", p->Reg.Chave,
                   p->Dir->Reg.Chave);
            exit(1);
        }
    }
    TestaI(p->Esq);
    TestaI(p->Dir);
}

void Testa(TipoNo *p) {
    if (p != NULL)
        TestaI(p);
}