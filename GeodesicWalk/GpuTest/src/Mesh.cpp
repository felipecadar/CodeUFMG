#include "Mesh.h"

void Vec3::myCudaFunciton(Vec3 a, Vec3 b, Vec3 c){
	#ifdef GPU
		myfunction_GPU(a, b, c);
	#else
		printf("CPU math! \n");
	#endif
}
