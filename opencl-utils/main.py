import os
import numpy as np
import pyopencl as cl
os.environ["PYOPENCL_CTX"] = '0'

if __name__ == "__main__":

    # Random inputs
    lenth = np.int32(10)

    n_vec1 = np.int32(4)
    n_vec2 = np.int32(4)

    arr1 = np.random.random_sample([n_vec1, lenth]).astype(np.float32) # Be careful with types!
    arr2 = np.random.random_sample([n_vec2, lenth]).astype(np.float32) # Be careful with types!

    # Output matrix
    res = np.zeros([n_vec1, n_vec2],  dtype=np.float32) # Be careful with types!

    # Build env
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags

    # Create OpenCL variables that points to numpy arrays
    arr1_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=arr1.flatten())
    arr2_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=arr2.flatten())

    # Create Output OpenCL variable with corret size
    res_cl = cl.Buffer(ctx, mf.WRITE_ONLY, res.nbytes)

    # Load and compile OpenCL program
    program = cl.Program(ctx,open("prog.cl", "r").read()).build()

    # Call kernel functions from the program with:    
    # f(queue, Global kernel size tuple(X, [Y, [Z]]), Local Kernel size (None), *args...)
    program.distMat(queue, res.shape, None, arr1_cl, arr2_cl, res_cl, n_vec1, lenth)
    
    # Wait for finish
    queue.finish()

    # Copy from GPU
    cl.enqueue_copy(queue, res, res_cl)

    print(res)
    # print(np.sum(np.linalg.norm(arr1-arr2, axis=1)))