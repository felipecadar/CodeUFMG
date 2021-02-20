#include "operations_mat.h"
#include <string.h>

int *alloc_vec(int size)
{
    int *vec;
    vec = (int *)malloc(sizeof(int *) * size);
    return vec;
}

tuple **alloc_mat(int size)
{
    tuple **mat;
    int i, j;

    mat = (tuple **)malloc(sizeof(tuple *) * size);
    for (i = 0; i < size; i++)
    {
        mat[i] = (tuple *)malloc(sizeof(tuple) * size);
    }

    for (i = 0; i < size; i++)
    {
        for (j = 0; j < size; j++)
        {
            mat[i][j].sum = 0;
            mat[i][j].min = 0;
            mat[i][j].max = 0;
        }
    }

    return mat;
}

void print_vec(int *vec, int size)
{
    int i;
    for (i = 0; i < size; i++)
    {
        printf("%d ", vec[i]);
    }
    printf("\n");
}

void print_mat(tuple **mat, int size){
    int i, j;
    printf("\n-------------------------------------------------------------------------------------------\n");
    for (i = 0; i < size; i++)
    {
        for (j = 0; j < size; j++){
            printf("(%2d, %2d, %2d) ", mat[i][j].min, mat[i][j].max, mat[i][j].sum);
        }
        printf("\n");
    }
    printf("\n-------------------------------------------------------------------------------------------\n");
}

void calc_interval(int init, int end, tuple **mat, int *vec)
{
    int i, sum, min, max, tmp;

    // find max
    max = vec[init];
    min = vec[init];
    sum = 0;

    for (i = init; i <= end; i++){
        max = (vec[i] > max ) ? vec[i] : max;
        min = (vec[i] < min ) ? vec[i] : min;
        sum += vec[i];
    }

    // save values
    mat[init][end].sum = sum;
    mat[init][end].min = min;
    mat[init][end].max = max;

}

void sub(int init, int end, tuple **mat, int *vec, int size)
{
    int i, j;

    // sub each element
    for (i = init; i <= end; i++)
    {
        vec[i]--;
    }

    // recalculate matrix for this interval
    for (i = 0; i < size; i++)
    {
        for (j = i; j < size; j++)
        {
            if (intersection(i, j, init, end)) {
                calc_interval(i, j, mat, vec);
            }
        }
    }
}
void add(int init, int end, tuple **mat, int *vec, int size)
{

    int i, j;

    // sub each element
    for (i = init; i <= end; i++)
    {
        vec[i]++;
    }

    // recalculate matrix for this interval
    for (i = 0; i < size; i++)
    {
        for (j = i; j < size; j++)
        {
            if (intersection(i, j, init, end)) {
                calc_interval(i, j, mat, vec);
            }
        }
    }
}
int min(int init, int end, tuple **mat)
{
    return mat[init][end].min;
}
int max(int init, int end, tuple **mat)
{
    return mat[init][end].max;
}
int sum(int init, int end, tuple **mat)
{
    return mat[init][end].sum;
}

int check_operation(char *operation)
{
    if (!strcmp(operation, "Sub"))
    {
        return 1;
    }
    if (!strcmp(operation, "Add"))
    {
        return 2;
    }
    if (!strcmp(operation, "Min"))
    {
        return 3;
    }
    if (!strcmp(operation, "Max"))
    {
        return 4;
    }
    if (!strcmp(operation, "Sum"))
    {
        return 5;
    }
    return -1;
}

int run_operation(int init, int end, tuple **mat, int *vec, int size, char *operation)
{
    int op, result;
    op = check_operation(operation);
    // printf("Op: %s \n", operation);

    switch (op)
    {
    case 1:
        sub(init, end, mat, vec, size);
        return 1;
        break;

    case 2:
        add(init, end, mat, vec, size);
        return 1;
        break;

    case 3:
        result = min(init, end, mat);
        break;

    case 4:
        result = max(init, end, mat);
        break;

    case 5:
        result = sum(init, end, mat);
        break;

    default:
        return 0;
    }

    printf("%d\n", result);
    return 1;
}

void free_vec(int *vec)
{
    free(vec);
}

void free_mat(tuple **mat, int size)
{
    int i;
    for (i = 0; i < size; i++)
    {
        free(mat[i]);
    }
    free(mat);
}

int intersection(int init, int final, int desired_init, int desired_final)
{
    if (final < desired_init || init > desired_final)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}