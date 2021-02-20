#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <sys/time.h>
#include <pthread.h>
#include <semaphore.h> 

typedef long TipoChave;

typedef struct TipoRegistro {
  TipoChave Chave;
  /* outros componentes */
} TipoRegistro;

typedef struct TipoNo * TipoApontador;

typedef struct TipoNo {
  TipoRegistro Reg;
  TipoApontador Esq, Dir;
  
  sem_t area;
  sem_t rmutex;
  sem_t ordering;
  long readCount;

} TipoNo;
typedef TipoApontador TipoDicionario;

void Pesquisa(TipoRegistro *x, TipoApontador *p);
void Insere(TipoRegistro x, TipoApontador *p);
void Inicializa(TipoApontador *Dicionario);
void Antecessor(TipoApontador q, TipoApontador *r);
void Retira(TipoRegistro x, TipoApontador *p);
void Central(TipoApontador p);
void CentralSem(TipoApontador p);
double rand0a1();
void Permut( TipoChave A[], int n);

void TestaI(TipoNo *p);
void Testa(TipoNo *p);