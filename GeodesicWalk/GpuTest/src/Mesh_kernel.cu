#include <stdio.h>
#include "cuda_runtime.h"

extern "C"{
    #include "structs.h"
}

__global__ void kernel() {
    printf("Hello, from the GPU! \n");
}

extern "C" void myfunction_GPU(Vec3 a, Vec3 b, Vec3 c) {

    printf("Cuda -> %.2f\n", a.dot(b));

    kernel<<<1,1>>>();
    cudaDeviceSynchronize();
}