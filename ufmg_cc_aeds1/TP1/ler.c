#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char const *argv[]){	

	FILE *file;
	file = fopen(argv[1], "r");
	char line[1024];
	char *value;

	fgets(line, sizeof(line), file);
	
	while (fgets(line, sizeof(line), file)){

		value = strtok(line, ";");
		printf("%s\n", value);

		while(value != '\n'){

		value = strtok(NULL, ";");
		printf("%s\n", value);

		}
	}

return 0;
}