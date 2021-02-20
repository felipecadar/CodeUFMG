#include "Mesh.h"

int main(void)
{

	Vec3 a(1.0, 0.0, 0.0);
	Vec3 b(0.0, 1.0, 0.0);
	Vec3 c(0.0,0.0,1.0);

	Vec3 v = a.cross(b);

    v.myCudaFunciton(a, b, c);

	printf("Cpp -> %.2f\n", a.dot(b));
	printf("%.2f, %.2f, %.2f\n", v.x, v.y, v.z);

	return 0;
}
