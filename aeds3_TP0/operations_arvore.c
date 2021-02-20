#include <operations_arvore.h>
#include <string.h>
#include <math.h>

int *alloc_vec(int size)
{
    int *vec;
    vec = (int *)malloc(sizeof(int) * size);
    return vec;
}

tuple *alloc_tree(int size)
{
    tuple *vec;
    vec = (tuple *)malloc(sizeof(tuple) * size);
    return vec;
}

void construct_segtree(tuple *tree, int *vec, int node, int init, int final)
{
    int middle = (int)((final + init) / 2);

    tree[node].init = init;
    tree[node].final = final;

    if ((final - init) == 0)
    {
        tree[node].max = vec[init];
        tree[node].min = vec[init];
        tree[node].sum = vec[init];
        
    }
    else
    {

        //next nodes (index starts at zero)
        int left  = (2 * node) + 1;
        int right = (2 * node) + 2;

        construct_segtree(tree, vec, left, init, middle);
        construct_segtree(tree, vec, right, middle + 1, final);

        tree[node].min = (tree[left].min < tree[right].min) ? tree[left].min : tree[right].min;
        tree[node].max = (tree[left].max > tree[right].max) ? tree[left].max : tree[right].max;
        tree[node].sum =  tree[left].sum + tree[right].sum;
    }

}

int min(tuple *tree, int node, int desired_init, int desired_final)
{

    int init = tree[node].init;
    int final = tree[node].final;

    // printf(GRN "Min operation | [ %d %d ] | " RESET, init, final);

    if (init >= desired_init && final <= desired_final)
    {
        return tree[node].min;
    }
    else if (intersection(init,final, desired_init, desired_final))
    {
        //next nodes (index starts at zero)
        int left = 2 * node + 1;
        int right = 2 * node + 2;

        // return next min
        int left_int = min(tree, left, desired_init, desired_final);
        int right_int = min(tree, right, desired_init, desired_final);

        return (left_int < right_int) ? left_int : right_int;
    }
    else
    {
        // outside the desired range -> return min int
        return 2147483647;
    }
}

int max(tuple *tree, int node, int desired_init, int desired_final)
{

    int init = tree[node].init;
    int final = tree[node].final;


    if (init >= desired_init && final <= desired_final)
    {
        return tree[node].max;
    }
    else if (intersection(init,final, desired_init, desired_final))
    {
        //next nodes (index starts at zero)
        int left = 2 * node + 1;
        int right = 2 * node + 2;

        // return next max
        int left_int = max(tree, left, desired_init, desired_final);
        int right_int = max(tree, right, desired_init, desired_final);

        return (left_int > right_int) ? left_int : right_int;
    }
    else
    {
        // outside the desired range -> return max int
        return -2147483648;
    }
}

int sum(tuple *tree, int node, int desired_init, int desired_final)
{

    int init = tree[node].init;
    int final = tree[node].final;

    if (init >= desired_init && final <= desired_final)
    {
        return tree[node].sum;
    }
    else if (intersection(init,final, desired_init, desired_final))
    {
        //next nodes (index starts at zero)
        int left = 2 * node + 1;
        int right = 2 * node + 2;

        // return next sum
        int left_int = sum(tree, left, desired_init, desired_final);
        int right_int = sum(tree, right, desired_init, desired_final);

        return left_int + right_int;
    }
    else
    {
        // outside the desired range -> return sum int
        return 0;
    }
}

int add(tuple *tree, int node, int desired_init, int desired_final)
{
    int init = tree[node].init;
    int final = tree[node].final;

    
    if (intersection(init, final, desired_init, desired_final))
    {
        //needs to change
        if (init == final)
        {
            tree[node].min++;
            tree[node].max++;
            tree[node].sum++;
        }
        else
        {
            //next nodes (index starts at zero)
            int left  = (2 * node) + 1;
            int right = (2 * node) + 2;
            
            add(tree, left, desired_init, desired_final);
            add(tree, right, desired_init, desired_final);
            
            
            tree[node].min = (tree[left].min < tree[right].min) ? tree[left].min : tree[right].min;
            tree[node].max = (tree[left].max > tree[right].max) ? tree[left].max : tree[right].max;
            tree[node].sum = tree[left].sum + tree[right].sum;
        }
    }
}

int sub(tuple *tree, int node, int desired_init, int desired_final)
{
    int init = tree[node].init;
    int final = tree[node].final;
    
    if (intersection(init, final, desired_init, desired_final))
    {
        //needs to change
        if (init == final)
        {
            tree[node].min--;
            tree[node].max--;
            tree[node].sum--;
        }
        else
        {
            //next nodes (index starts at zero)
            int left = 2 * node + 1;
            int right = 2 * node + 2;
            
            sub(tree, left, desired_init, desired_final);
            sub(tree, right, desired_init, desired_final);
            
            tree[node].min = (tree[left].min < tree[right].min) ? tree[left].min : tree[right].min;
            tree[node].max = (tree[left].max > tree[right].max) ? tree[left].max : tree[right].max;
            tree[node].sum = tree[left].sum + tree[right].sum;
        }
    }
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

int run_operation(tuple *tree, int *vec, int init, int final, int vec_size, char *operation)
{
    int op, result;
    op = check_operation(operation);

    switch (op)
    {
    case 1:
        sub(tree, 0, init, final);
        return 1;
        break;

    case 2:
        add(tree, 0, init, final);
        return 1;
        break;

    case 3:
        result = min(tree, 0, init, final);
        break;

    case 4:
        result = max(tree, 0, init, final);
        break;

    case 5:
        result = sum(tree, 0, init, final);
        break;

    default:
        return 0;
    }

    printf("%d\n", result);
    return 1;
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