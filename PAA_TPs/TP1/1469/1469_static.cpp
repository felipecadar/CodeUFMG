#include <iostream>
#include<string.h>

#define MAX_N 500
#define MAX_M (60*103)
using namespace std;


void change(int G[MAX_N][MAX_N], int N, int arg1, int arg2){
    // cout << "Change: "<< arg1 << "-" << arg2 << endl;
    // cout << "Before" << endl;
    // printG(G, N);
    int tmp;
    for (int i = 0; i < N; i++)
        swap(G[arg1][i], G[arg2][i]);
    for (int i = 0; i < N; i++)
        swap(G[i][arg1], G[i][arg2]);
    
    // cout << "After" << endl;
    // printG(G, N);
}

void backprop(int G[MAX_N][MAX_N], int K[MAX_N], int N, int i, int &min, int visited[MAX_N]){
    // printf("Got In! N=%i, i=%i\n", N, i);
    for (int j = 0; j < N; j++)
    {
        if (G[j][i] == 1 && visited[j] == 0){
            visited[j] = 1;
            if(K[j] < min || min == 0){
                min = K[j];
            }
            backprop(G, K, N, j, min, visited);
        }
    }
}


int main(int argc, char const *argv[])
{   

    int N, M, I, x, y;
    int K[MAX_N];
    int G[MAX_N][MAX_N] = {0};
    int visited[MAX_N] = {};
    while(scanf("%i %i %i", &N, &M, &I) > 0){
        memset(K, 0, sizeof(K));
        for (int i = 0; i < N; i++)
        {
            scanf("%i", &K[i]);
        }

        memset(G, 0, sizeof(G));
        for (int i = 0; i < M; i++)
        {
            scanf("%i %i", &x, &y);
            x--;y--;
            G[x][y] = 1;
        }
        // printG(G, N);

        // printG(G, N);
        // Intructions

        for (int i = 0; i < I; i++)
        {   
            char opt[2];
            int arg1, arg2;
            scanf("%s", opt);

            if(opt[0] == 'P'){
                scanf("%i", &arg1);
                int min = 0;
                // cout << "P " << arg1-1<< "-> ";
                memset(visited, 0, sizeof(visited));
                backprop(G, K, N, arg1-1, min, visited);
                if(min > 0){
                    cout << min << endl;
                }else{
                    cout << "*" << endl;
                }
            }
            if(opt[0] == 'T'){
                scanf("%i %i", &arg1, &arg2);
                change(G, N, arg1-1, arg2-1);
                // cout << "T " << arg1-1 << " " << arg2-1 << endl;
                // printG(G, N);
            }
        }
        
    }

    return 0;
}
