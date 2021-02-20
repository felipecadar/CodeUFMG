#ifndef STRUCTS_H
#define STRUCTS_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

class Vec3
{
	public:

	 double x, y, z;

		void myCudaFunciton(Vec3 a, Vec3 b, Vec3 c);

		Vec3(double _x, double _y, double _z)
		{
			x = _x;  y = _y;  z = _z;
		}

		Vec3() {}

		double norm()
		{
			return sqrt(x * x + y * y + z * z);
		}

		Vec3 unit()
		{
			double l = norm();
			return Vec3(x/l, y/l, z/l);
		}
		
		Vec3 operator+(const Vec3 &v)
		{
			return Vec3(x + v.x,  y + v.y,  z + v.z);
		}

		Vec3 operator-(const Vec3 &v)
		{
			return Vec3(x - v.x,  y - v.y,  z - v.z);
		}

		double dot(const Vec3 &v)
		{
			return x * v.x + y * v.y + z * v.z;
		}

		Vec3 cross(const Vec3 &v)
		{
			return Vec3(y * v.z - z * v.y, z * v.x - x * v.z, x * v.y - y * v.x);
		}

};


#endif