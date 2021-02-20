#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "operations_mat.h"

int main()
{
    int vec_size, i, j, init, end, scan, *vec, inquiries, success;
    tuple **mat;
    char *operation;    

    scan = scanf("%d %d", &vec_size, &inquiries);
    if (!scan)
    { //fail to scanf stdin
        return -1;
    }

    // allocate array and matrix
    vec = alloc_vec(vec_size);
    mat = alloc_mat(vec_size);

    //fill array
    for (i = 0; i < vec_size; i++)
    {
        scan = scanf("%d", &vec[i]);
        if (!scan)
        {//fail to scanf stdin
            return -1;
        }
    }
    
    //calculate first matrix
    for (i = 0; i < vec_size; i++){
        for (j = i; j < vec_size; j++){
            calc_interval(i, j, mat, vec);
        }
    }

    // iterate over each inquirie

    operation = (char*)malloc(sizeof(char) * 4);
    for (i = 0; i < inquiries; i++){
        scan = scanf("%s %d %d", operation, &init, &end);
        if (!scan)
        {//fail to scanf stdin
            printf("Fail to scan...\n");
            return -1;
        }     
        
        // change index from 1 to 0
        init--;
        end--;
        // printf("Command: %s %d %d\n", operation, init, end);
        success = run_operation(init, end, mat, vec, vec_size, operation);
        // print_vec(vec, vec_size);
        if(!success){
            printf("Invalid Operation [' %s '] ! \n", operation);
        }
        // print_mat(mat, vec_size);
    }
    

    //free array and matrix
    free_mat(mat, vec_size);
    free_vec(vec);
    free(operation);

    return 0;
}