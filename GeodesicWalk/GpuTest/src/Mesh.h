#ifndef MESH_H
#define MESH_H

#include <set>
#include <vector>
#include <algorithm>
#include <string>
#include <iostream>
#include <fstream>
#include <math.h>
#include <stdio.h>
#include "structs.h"


#ifdef GPU
extern "C" 
{
	void myfunction_GPU(Vec3 a, Vec3 b, Vec3 c);
}
#endif



#endif