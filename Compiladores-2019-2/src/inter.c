#include <stdlib.h>
#include <stdio.h>

//Registers
#define CB 0
#define CT 1
#define PB 2
#define PT 3
#define SB 4
#define ST 5
#define HB 6
#define HT 7
#define LB 8
#define L1 9
#define L2 10
#define L3 11
#define L4 12
#define L5 13
#define L6 14
#define CP 15

//Instructions
#define LOAD 	 0
#define LOADA 	 1
#define LOADI 	 2
#define LOADL 	 3
#define STORE 	 4
#define STOREI 	 5
#define CALL 	 6
#define CALLI 	 7
#define RETURN 	 8
#define PUSH 	 9
#define POP 	10
#define JUMP 	11
#define JUMPI 	12
#define JUMPIF 	13
#define HALT 	14

int num_args = 0;

void proced_end() {
	printf("%d 0 0 %d\n", RETURN, num_args);
}

void proced_begin() {
	num_args = 0;
}

void atrib(int p1, int p2) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d %d 1\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, p2);
	
}

void param(int p1) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	num_args++;
}

void call(int p1) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d 0 0 0\n", CALLI);	
}

void igual(int p1, int p2, int result) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d %d 17\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, result);
}

void goto_(int p1) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d 0 0 0\n", JUMPI);
}

void mais(int p1, int p2, int result) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d %d 8\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, result);
}

void vezes(int p1 , int p2 , int result) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d %d 10\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, result);
}

void menos(int p1, int p2, int result) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d %d 9\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, result);
}

void div_(int p1, int p2, int result) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d %d 11\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, result);
}

void ou(int p1, int p2, int result) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d %d 4\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, result);
}

void e(int p1, int p2, int result) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d %d 3\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, result);
}

void nega(int p1, int p2) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d %d 2\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, p1);
}

void prog_end() {
	printf("%d 0 0 0\n", HALT);
}
  
void go_true(int p1, int p2) {
	printf("%d %d 1 %d\n", LOAD, ST, p2);
	printf("%d %d 1 %d\n", JUMPIF, CB, p1);
}

void write_char(int p1, int p2) {
	int i = 0;
	printf("%d %d 1 %d\n", LOAD, ST, p1);

	while (i < p2) {
		printf("%d %d %d 22\n", CALL, PB, CB);
		printf("%d 0 0 1\n", LOADL);
		printf("%d %d %d 14\n", CALL, PB, CB);

		i++;
	}
}
  
void read_int(int p1) {
	printf("%d %d %d 25\n", CALL, PB, CB);
	printf("%d %d 1 %d\n", STORE, ST, p1);
}
  
void write_int(int p1) {
	printf("%d %d 1 %d\n", LOAD, ST, p1);
	printf("%d %d %d 26\n", CALL, PB, CB);
}

int main() {
	proced_end();
}