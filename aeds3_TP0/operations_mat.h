#include <stdio.h>
#include <stdlib.h>

typedef struct tuple{
    int sum;
    int min;
    int max;
}tuple;


int* alloc_vec(int size);
tuple **alloc_mat(int size);
void calc_interval(int init, int end, tuple **matrix, int *vec);

void sub(int init, int end, tuple **mat, int *vec, int size);
void add(int init, int end, tuple **mat, int *vec, int size);
int min(int init, int end, tuple **mat);
int max(int init, int end, tuple **mat);
int sum(int init, int end, tuple **mat);

int check_operation(char *operation);
int run_operation(int init, int end, tuple **mat, int *vec, int size, char *operation);
int intersection(int init, int final, int desired_init, int desired_final);


void print_vec(int *vec,  int size);
void print_mat(tuple **mat, int size);
    
void free_vec(int *vec);
void free_mat(tuple **mat, int size);
    
    