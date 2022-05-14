#define DEBUG

#include <stdio.h>
#include <string.h>

#include <algorithm>
#include <iostream>

#define MAX_N 101
#define INF 99999
using namespace std;

void printMatrix(int matrix[MAX_N][MAX_N][MAX_N], int N, int k) {
    printf("         ");
    for (int i = 0; i < N; i++)
    {
        printf(" [%2d] ", i+1);
    }
    printf("\n");
    
    for (int i = 0; i < N; i++) {
        printf(" [%4d] ", i+1);
        for (int j = 0; j < N; j++) {
            if (matrix[k][i][j] == INF)
                printf(" %4s ", "INF");
            else
                printf(" %4d ", matrix[k][i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int main(int argc, char const *argv[]) {
    int N, M;
    int A, B, W;
    int C;

    int G[MAX_N][MAX_N];
    int dist[MAX_N][MAX_N][MAX_N];
    int pred[MAX_N][MAX_N];
    int inst = 0;

    while (scanf("%d %d", &N, &M) > 0) {
        memset(G, INF, MAX_N * MAX_N);
        memset(dist, INF, MAX_N * MAX_N * MAX_N);

        fill_n(&G[0][0], MAX_N*MAX_N, INF);
        fill_n(&dist[0][0][0], MAX_N*MAX_N*MAX_N, INF);

        printf("Instancia %d\n", ++inst);
        for (int i = 0; i < M; i++) {
            scanf("%d %d %d", &A, &B, &W);
            A--;
            B--;

            if (G[A][B] > -1) {
                G[A][B] = min(G[A][B], W);
            dist[0][A][B] = W;
            } else {
                G[A][B] = W;
            }

            dist[0][A][B] = G[A][B];
        }

        for (int i = 0; i < N; i++) {
            G[i][i] = 0;
            dist[0][i][i] = 0;
        }

        // printf("K = %d\n", 0);
        // printMatrix(dist, N, 0);
        for (int k = 0; k < N; k++) {
            // printf("K = %d\n", k);
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    dist[k][i][j] = dist[k-1][i][j];
                    if (i != j && i != k && j != k) {
                        if(k == 0){
                            dist[k][i][j] = min(G[i][j], G[i][k] + G[k][j]);
                        }else{
                            dist[k][i][j] = min(dist[k - 1][i][j], dist[k - 1][i][k] + dist[k - 1][k][j]);
                        }
                        // printf("[%d->%d:%d] %d->%d:%d  %d->%d:%d \n", i+1, j+1, dist[k - 1][i][j], i+1, k+1, dist[k - 1][i][k], k+1, j+1, dist[k - 1][k][j]);
                    }
                }
            }
            // printMatrix(dist, N, k);
        }

        scanf("%d", &C);
        int FROM, TO, BY;
        for (int i = 0; i < C; i++) {
            scanf("%d %d %d", &FROM, &TO, &BY);

            // printf("From:%d To:%d By:%d\n", FROM, TO, BY);
            FROM--;
            TO--;
            
            if (BY == 0) {
                printf("%d\n", G[FROM][TO] != INF ? G[FROM][TO] : -1);
            } else {
                BY--;
                // printf("From:%d To:%d By:%d\n", FROM, TO, BY);
                // printMatrix(dist, N, BY);

                int w = dist[BY][FROM][TO];
                printf("%d\n", w == INF ? -1 : w);
            }
        }

        printf("\n");
    }

    return 0;
}
