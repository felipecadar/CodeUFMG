#include <stdio.h>
#include <stdlib.h>

typedef struct tuple{
    // Internval propriets
    int sum;
    int min;
    int max;

    // Internval
    int init;
    int final;
}tuple;


// Alloc vector with desired size
int *alloc_vec(int size);
tuple *alloc_tree(int size);

void construct_segtree(tuple *tree, int *vec, int node, int init, int final);

int check_operation(char *operation);
int run_operation(tuple *tree, int *vec, int init, int final, int vec_size, char *operation);

int min(tuple *tree, int node, int desired_init, int desired_final);
int max(tuple *tree, int node, int desired_init, int desired_final);
int sum(tuple *tree, int node, int desired_init, int desired_final);
void add(int init, int end, tuple **mat, int *vec, int size);
int sub(tuple *tree, int node, int desired_init, int desired_final);


int intersection(int init, int final, int desired_init, int desired_final);
        