#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#define NMax 100       
int escop[10];
int TabHash[509];
int level;              
int L;                  
int Root;               
struct
{
    char name[10];      
    int level;          
    char atr[10];  
    int col;
} TableS[100];         

void InBlock();
void Error(int num);
void OutBlock();
void GetEntry(char name[10]);
void Put(char name[10], char atr[10]);
void printAll(void);

void main(){
    L = 1;
    Root = 0;
    level = 1;
    escop[level] = 1;
}

void Error(int num){
    if(num == 1){
        printf("Full Table\n");
    }else if (num == 2){
        printf("Not Found\n");
    }else if (num == 3){
        printf("Already Inserted\n");
    }
}

void InBlock(){
    level++;
    if(level>NMax){
        Error(1);
    }
    else{
        escop[level] = L;
    }
}

void OutBlock()
{
    int S, B, k;
    char ident[10];
    S = L;
    B = escop[level];
    while (S > B)    {
        S--;
        strcpy(ident, TableS[S].name);
        k = ident[1];
        TabHash[k] = TableS[S].col;
    }
    level--;
    L = B;
}
void GetEntry(char x[10])
{
    int n, aux, achou, k;
    achou = 0;
    n = x[0];
    k = TabHash[n];
    while ((k != 0) && (achou == 0)){
        aux = strcmp(TableS[k].name, x);
        if (aux == 0){
            achou = 1;
        }
        else{
            k = TableS[k].col;
        }
    }
    if (achou == 1)
    {
        printf("Level: %d -- Index: %u \n", TableS[k].level, k);
    }
    else{
        Error(2);
    }
}
void Put(char X[10], char atribut[10])
{
    int n, igual, k, aux;
    igual = 0;
    n = X[0]; /* Calcula o hashing(X)*/
    k = TabHash[n];
    while (k >= escop[level]){
        aux = strcmp(TableS[k].name, X);
        if (aux == 0)
        {
            Error(3);
            igual = 1;
        }
        k = TableS[k].col;
    }
    if (L == NMax + 1){
        Error(1);
    }
    else if (igual == 0){
        TableS[L].level = level;
        aux = strlen(atribut);
        for (k = 0; k <= aux - 1; k++){
            TableS[L].atr[k] = atribut[k];
        }

        aux = strlen(X);
        for (k = 0; k <= (aux - 1); k++){
            TableS[L].name[k] = X[k];
        }

        TableS[L].col = TabHash[n];
        TabHash[n] = L;
        L++;
    }
}
void printAll()
{
    for (int i = 0; i <= L; i++)
    {
        printf("########################################\n");
        printf("Name: %s | Atr: %s | Level %s \n", TableS[i].name, TableS[i].atr, TableS[i].level);
        printf("########################################\n");
    }
}