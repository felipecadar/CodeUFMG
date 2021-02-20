#include "hash.h"

struct Team{
    char name[1024*100];
    int id;
    int vit;
    int sg;
    int gp;
    int score;
};
typedef struct Team team;

void ler_rodada(FILE *f, int rounds, int SIZE, hashTable *hashArray[], team times[], int t_number);
void quick_sort(team *a, int left, int right) ;
void shell_sort(team *a, int size);
int alf(char *str1, char *str2);

void quicksort_alt(team v[], int esq, int dir);
int particao(team v[],int esq,int dir);
void troca(team v[], int i,int j);
