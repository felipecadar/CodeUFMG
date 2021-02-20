#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "operations_arvore.h"

int main()
{
    int vec_size, tree_size, i, j,init, end, scan, *vec, inquiries, success;
    // segtree *root;
    char operation[5];
    tuple *tree;

    scan = scanf("%d %d", &vec_size, &inquiries);
    if (!scan)
    { //fail to scanf stdin
        return -1;
    }

    //aprox number of nodes in the segtree
    tree_size = ( vec_size * 4 ) - 1;
    
    // printf("Vec_size %d Tree_size %d\n", vec_size, tree_size);
    
    // allocate array and matrix
    vec  = (int *)calloc(sizeof(int) , vec_size);
    tree = (tuple *)calloc(sizeof(tuple), tree_size);

    for(i = 0; i < tree_size; i++){
        tree[i].max = 0;
        tree[i].min = 0;
        tree[i].sum = 0;

        tree[i].init = -1;
        tree[i].final = -2;
    }

    //fill array
    for (i = 0; i < vec_size; i++)
    {
        scan = scanf("%d", &vec[i]);
        if (!scan)
        { //fail to scanf stdin
            return -1;
        }
    }

    // construct segmentation tree
    construct_segtree(tree, vec, 0, 0, vec_size-1);
    // printf("-------------------------------------------------------------------------------------\n");

    // iterate over each inquirie
    for (i = 0; i < inquiries; i++)
    {
        scan = scanf("%s %d %d", operation, &init, &end);
        if (!scan)
        { //fail to scanf stdin
            printf("Fail to scan...\n");
            return -1;
        }

        // change index from 1 to 0 (Make things easer)
        init--;
        end--;

        success = run_operation(tree, vec, init, end, vec_size, operation);
        
        if (!success)
        {
            printf("Invalid Operation [' %s '] ! \n", operation);
        }
        // printf("-------------------------------------------------------------------------------------\n");
    }

    //free arrays
    // free(operation);
    free(vec);
    // free(tree);
    

    return 0;
}
