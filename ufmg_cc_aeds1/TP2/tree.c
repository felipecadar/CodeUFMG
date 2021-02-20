#include <stdio.h>
#include <stdlib.h>
#include "tree.h"
#define FALSE 0
#define TRUE 1

struct sbb buscarArvore(struct sbb *A, int chave, FILE *out){       //BUSCA NA ARVORE

    if(A != NULL && A->reg.colision_key == chave){
        char value[50];

        strcpy(value, A->reg.team1);

        fprintf(out,"%s;%s;%i;%s;%i\n",strtok(A->reg.data, A->reg.team1), value, A->reg.team1_g, A->reg.team2, A->reg.team2_g);


    }

    if(A != NULL && A->dir != NULL && A->dir->reg.chave > A->reg.chave ){  //BUSCA NA DIREITA
        buscarArvore(A->dir, chave, out);
    }

    if(A != NULL && A->esq != NULL && A->esq->reg.chave < A->reg.chave){  //BUSCA NA ESQUERDA
        buscarArvore(A->esq, chave, out);
    }


}


struct sbb ee(struct sbb *ptr)      //BALANCEIA ESQUERDA ESQUERDA
{
    struct sbb *tmp = (struct sbb*)malloc(sizeof(struct sbb));

    (*tmp).reg = (*ptr).esq->reg;

    tmp->dir =(struct sbb*) malloc(sizeof(struct sbb));
    (*tmp).dir->reg = (*ptr).esq->esq->reg;

    tmp->esq =( struct sbb*)malloc(sizeof(struct sbb));
    (*tmp).esq->reg = (*ptr).reg;

    return *tmp;
}

struct sbb dd(struct sbb *ptr) //BALANCEIA DIREITA DIREITA
{
    struct sbb *tmp = (struct sbb*)malloc(sizeof(struct sbb));

    (*tmp).reg = (*ptr).dir->reg;

    tmp->dir =(struct sbb*) malloc(sizeof(struct sbb));
    (*tmp).dir->reg = (*ptr).dir->dir->reg;

    tmp->esq =( struct sbb*)malloc(sizeof(struct sbb));
    (*tmp).esq->reg = (*ptr).reg;

    return *tmp;

}

struct sbb ed(struct sbb *ptr) //BALANCEIA ESQUERDA DIREITA
{

    struct sbb *tmp = (struct sbb*)malloc(sizeof(struct sbb));

    (*tmp).reg = (*ptr).esq->dir->reg;

    tmp->dir =(struct sbb*) malloc(sizeof(struct sbb));
    (*tmp).dir->reg = (*ptr).esq->reg;

    tmp->esq =( struct sbb*)malloc(sizeof(struct sbb));
    (*tmp).esq->reg = (*ptr).reg;

    return *tmp;
}

struct sbb de(struct sbb *ptr) //BALANCEIA DIREITA ESQUERDA
{
    struct sbb *tmp = (struct sbb*)malloc(sizeof(struct sbb));

    (*tmp).reg = (*ptr).dir->esq->reg;

    tmp->dir =(struct sbb*) malloc(sizeof(struct sbb));
    (*tmp).dir->reg = (*ptr).dir->reg;

    tmp->esq =( struct sbb*)malloc(sizeof(struct sbb));
    (*tmp).esq->reg = (*ptr).reg;

    return *tmp;

}

void iinsere_aqui (jogo reg, struct sbb **ptr, int *incli, int *fim)
{
    struct sbb *no =(struct sbb *) malloc(sizeof(struct sbb));

    no->reg = reg;
    no->esq = NULL;
    no->dir = NULL;
    no->esqtipo = SBB_VERTICAL;
    no->dirtipo = SBB_VERTICAL;
    *ptr = no;
    *incli = SBB_HORIZONTAL;
    *fim = FALSE;
}

void inicializa(struct sbb **raiz)  //INICIALIZA (NÃO É TOTALMENTE NECESSARIA MAS VALE A IMPLEMENTAÇÃO POR APRENDIZADO)
{
    *raiz = NULL;
}

void iinsere(jogo reg, struct sbb **ptr,int *incli, int *fim)

{
    if(*ptr == NULL)
    {
        iinsere_aqui(reg, ptr, incli, fim);
    } // achou onde inserir

    else if(reg.chave < (*ptr)->reg.chave)
    {
        iinsere(reg, &((*ptr)->esq), &((*ptr)->esqtipo), fim);
        if(*fim)
            return;
        if((*ptr)->esqtipo == SBB_VERTICAL)
        {
            *fim = TRUE;
        }
        else if((*ptr)->esq->esqtipo == SBB_HORIZONTAL)
        {
            **ptr = ee(*ptr);
            *incli = SBB_HORIZONTAL;
        }
        else if((*ptr)->esq->dirtipo == SBB_HORIZONTAL)
        {
            **ptr = ed(*ptr);
            *incli = SBB_HORIZONTAL;
        }

    }//veridica na parte esquerda da arvore

    else if(reg.chave > (*ptr)->reg.chave)
    {
        iinsere(reg, &((*ptr)->dir), &((*ptr)->dirtipo), fim);
        if(*fim)
            return;
        if((*ptr)->dirtipo == SBB_VERTICAL)
        {
            *fim = TRUE;
        }

        else if((*ptr)->dir->dirtipo == SBB_HORIZONTAL)
        {
            **ptr = dd(*ptr);
            *incli = SBB_HORIZONTAL;
        }
        else if((*ptr)->dir->esqtipo == SBB_HORIZONTAL)
        {
            **ptr = de(*ptr);
            *incli = SBB_HORIZONTAL;
        }
    }//verifica na parte direita da arvore

    else
    {
//        printf("ERRO: A chave ja esta na arvore\n");
        *fim = TRUE;
    } // a chave ja existe na arvore

}

void insere(jogo reg, struct sbb **raiz)
{
    int fim = FALSE;
    int inclinacao = SBB_VERTICAL;
    iinsere(reg, raiz, &inclinacao, &fim);
}
