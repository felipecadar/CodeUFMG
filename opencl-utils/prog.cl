float l2(__global const float *arr1, __global const float *arr2, const int length){
    // Calculates euclidian distance (L2) between descriptors
    //
    // arr1: single descriptor of size "lenght"
    // arr2: single descriptor of size "lenght"
    // lenght: descriptors size 
    // 
    // Returns float: l2 distance

    float s = 0;
    for(int i = 0; i < length; i++){
        float d = arr1[i] - arr2[i];
        s += d*d;
    }
    return sqrt(s);
}

int int_hamming(int x, int y)
{
    // Calculates hamming distances between bytes enconded by integers
    //
    // x: single int from binary descriptor
    // y: single int from binary descriptor
    //
    // Returns int: hamming distance

    int dist = 0;
    char val = x^y;// calculate differ bit
    while(val)   //this dist veriable calculate set bit in loop
    {
        ++dist; 
        val &= val - 1; 
    }
    return dist;
}

int hamming(__global const int *arr1, __global const int *arr2, const int length){
    // Calculates hamming distances between descriptors
    // 
    // arr1: single descriptor of size "lenght"
    // arr2: single descriptor of size "lenght"
    // lenght: descriptors size 
    // 
    // Returns int: hamming distance

    int counter = 0;
    for(int j=0; j < length; j++){
        counter += int_hamming(arr1[j], arr2[j]);
    }
    return counter;
}

int hammingRot(__global const int *arr1, __global const int *arr2, const int length, const int rotations){
    // Calculates minimun hamming distances between descriptors with rotation
    // 
    // arr1: single descriptor of shape ["lenght" X "rotations"]
    // arr2: single descriptor of shape ["lenght" X "rotations"]
    // lenght: descriptors size 
    // rotations: how many descriptors rotations needs to be conculatate 
    // 
    // Returns int: hamming distance

    int counter = length * 64;
    for(int i=0; i < rotations; i++){
        __global const int *arr2p = &(arr2[i * length]);

        int local_counter = hamming(arr1, arr2p, length);

        if (local_counter < counter){
            counter = local_counter;
        }
    }
    return counter;
}


// __kernel void distBwtVecs(__global const float *arr1, __global const float *arr2, __global float *result, const int length){
//     int gid = get_global_id(0);
//     result[gid] = l2(&arr1[gid * length], &arr2[gid * length], length);
// }


__kernel void distMat(__global const float *arr1, __global const float *arr2, __global float *result, const int n_vec1, const int length){
    // Calculate distance matrix between every descritor in arr1 to evert descriptor in arr2.
    // Uses float descriptors and calculates L2 distances.
    // "n_vec2" is not needed because its encodede in the OpenCL global id system.  
    // 
    // arr1 : matrix of descriptors of shape ["lenght" X "n_vec1"]
    // arr2 : matrix of descriptors of shape ["lenght" X "n_vec2"]
    // result : output matrix with results of shape ["n_vec1" X "n_vec2"]
    // n_vec1 : quantity of descriptor in "arr1"
    // length : length of one decriptor

    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);
    float d = l2(&arr1[gid_x * length], &arr2[gid_y * length], length);
    result[(gid_x * n_vec1) + gid_y] = d;
}

__kernel void distMatSym(__global const float *arr1, __global float *result, const int n_vec1, const int length){
    // Calculate distance matrix between every descritor in arr1 to every descritor in arr1;
    // Uses float descriptors and calculates L2 distances
    // This function exists because its take advantage of the symmetry of the result
    // 
    // arr1 : matrix of descriptors of shape ["lenght" X "n_vec1"]
    // result : output matrix with results of shape ["n_vec1" X "n_vec1"]
    // n_vec1 : quantity of descriptor in "arr1"
    // length : length of one decriptor

    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);

    if(gid_x <= gid_y){
        
        float d = l2(&arr1[gid_x * length], &arr1[gid_y * length], length);

        result[(gid_x * n_vec1) + gid_y] = d;
        result[(gid_y * n_vec1) + gid_x] = d;

    }
}

__kernel void distMatHamming(__global const int *arr1, __global const int *arr2, __global int *result, const int n_vec1, const int length){
    // Calculate distance matrix between every descritor in arr1 to evert descriptor in arr2.
    // Uses float descriptors and calculates hamming distances.
    // "n_vec2" is not needed because its encodede in the OpenCL global id system.  
    // 
    // arr1 : matrix of descriptors of shape ["lenght" X "n_vec1"]
    // arr2 : matrix of descriptors of shape ["lenght" X "n_vec2"]
    // result : output matrix with results of shape ["n_vec1" X "n_vec2"]
    // n_vec1 : quantity of descriptor in "arr1"
    // length : length of one decriptor

    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);
    int d = hamming(&arr1[gid_x * length], &arr2[gid_y * length], length);
    result[(gid_x * n_vec1) + gid_y] = d;
}

__kernel void distMatSymHamming(__global const int *arr1, __global int *result, const int n_vec1, const int length){
    // Calculate distance matrix between every descritor in arr1 to every descritor in arr2;
    // Uses int descriptors and calculates hamming distances
    // 
    // arr1 : matrix of descriptors of shape ["lenght" X "n_vec1"]
    // result : output matrix with results of shape ["n_vec1" X "n_vec1"]
    // n_vec1 : quantity of descriptor in "arr1"
    // length : length of one decriptor

    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);

    if(gid_x <= gid_y){
        
        int d = hamming(&arr1[gid_x * length], &arr1[gid_y * length], length);

        result[(gid_x * n_vec1) + gid_y] = d;
        result[(gid_y * n_vec1) + gid_x] = d;

    }
}

__kernel void distMatHammingRot(__global const int *arr1, __global const int *arr2, __global int *result, const int n_vec1, const int length, const int rotations){
    // Calculate distance matrix between every descritor in arr1 to evert descriptor in arr2 with rotations.
    // Uses float descriptors and calculates hamming distances.
    // "n_vec2" is not needed because its encodede in the OpenCL global id system.  
    // 
    // arr1 : matrix of descriptors of shape ["lenght" X "n_vec1"]
    // arr2 : matrix of descriptors of shape ["lenght" X "n_vec2"]
    // result : output matrix with results of shape ["n_vec1" X "n_vec2"]
    // n_vec1 : quantity of descriptor in "arr1"
    // length : length of one decriptor
    // rotations: how many descriptors rotations needs to be conculatate 

    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);
    int d = hammingRot(&arr1[gid_x * length], &arr2[gid_y * length], length, rotations);
    result[(gid_x * n_vec1) + gid_y] = d;
}

__kernel void distMatSymHammingRot(__global const int *arr1, __global int *result, const int n_vec1, const int length, const int rotations){
    // Calculate distance matrix between every descritor in arr1 to every descritor in arr2 with rotations;
    // Uses int descriptors and calculates hamming distances
    // 
    // arr1 : matrix of descriptors of shape ["lenght" X "n_vec1"]
    // result : output matrix with results of shape ["n_vec1" X "n_vec1"]
    // n_vec1 : quantity of descriptor in "arr1"
    // length : length of one decriptor
    // rotations: how many descriptors rotations needs to be conculatate 

    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);

    if(gid_x <= gid_y){
        
        int d = hammingRot(&arr1[gid_x * length], &arr1[gid_y * length], length, rotations);

        result[(gid_x * n_vec1) + gid_y] = d;
        result[(gid_y * n_vec1) + gid_x] = d;

    }
}