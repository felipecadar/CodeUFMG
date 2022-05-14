#define DEBUG

#include <iostream>
#include <string.h>
#include <limits.h>
#include <stdio.h>
#include <algorithm>

#ifdef DEBUG

#include <chrono>
typedef std::chrono::high_resolution_clock::time_point tvar;
tvar t1;
#define duration(a) std::chrono::duration_cast<std::chrono::nanoseconds>(a).count()
#define timeNow() std::chrono::high_resolution_clock::now()
#define setTime() t1 = timeNow()
#endif

#define MAX_N 1001
#define MAX_M (MAX_N*(MAX_N-1))/2
#define INF INT_MAX
using namespace std;

typedef struct Edge {
    int u, v, w;
} Edge;

int G[MAX_N][MAX_N];
Edge E[MAX_M];
int visited[MAX_N];
int sets[MAX_N];
int sum_visited = 0;

bool compareEdges(Edge x, Edge y){
    return x.w < y.w;
}

void visit(int N, int i){
    for (int j = 0; j < N; j++)
    {
        if (G[j][i] > 0 && visited[j] == 0){
            visited[j] = 1;
            sum_visited++;
            visit(N, j);
        }
    }
}

int testVisited(int N){
    if(sum_visited < N){
        cout << "impossivel" << endl;
        return 1;
    }
    return 0;
}

void printSet(int N){
    for (int i = 0; i < N; i++)
    {
        cout << sets[i] << " ";
    }
    cout << endl;
}

void setUnion(int u, int v, int N){
    int set_u = sets[u];
    int set_v = sets[v];
    for (int i = 0; i < N; i++)
    {
        if(sets[i] == set_v){
            sets[i] = set_u;
        }
    }
}

void kruskal(int N, int M){
    //make sets
    for (int i = 0; i < N; i++)
    {
        sets[i] = i;
    }
    
    // sort edges
    sort(E, E+M, compareEdges);
    
    int total_w = 0;
    int arestas = 0;
    // printSet(N);
    for (int i = 0; i < M; i++)
    {
        int u = E[i].u;
        int v = E[i].v;
        int w = E[i].w;
        // cout << w << " ";
        if(sets[u] != sets[v]){
            total_w += w;
            arestas += 1;
            // cout << "Union:" << u << "[" << sets[u] << "]" <<"x"<< v << "[" << sets[v] << "]"<< endl;
            setUnion(u, v, N);
            // printSet(N);
        }
    }

    if(arestas != N-1){
        cout << "impossivel" << endl;
    }else{
        cout << total_w << endl;
    }
    // cout << endl;
}



int main(int argc, char const *argv[])
{
    // ios_base::sync_with_stdio(false);

    int N,M;
    int a, b, c;
    while(scanf("%d %d", &N, &M) > 0){
        
        #ifdef DEBUG
        setTime();
        #endif
        memset(G, 0, sizeof(G));
        #ifdef DEBUG
        cout << "Memset G: " << (double)duration(timeNow()-t1)/1000000 << "ms" << endl;
        #endif

        #ifdef DEBUG
        setTime();
        #endif
        memset(visited, 0, sizeof(visited));
        #ifdef DEBUG
        cout << "Memset visited: " << (double)duration(timeNow()-t1)/1000000 << "ms" << endl;
        #endif

        // setTime();
        // for (int i = 0; i < MAX_M; i++){
        //     E[i].u = -1;
        //     E[i].v = -1;
        //     E[i].w = INF;
        // }
        // cout << "Set Edges " << (double)duration(timeNow()-t1)/1000000 << "ms" << endl;
        #ifdef DEBUG
        setTime();
        #endif
        for (int i = 0; i < M; i++)
        {
            scanf("%d %d %d", &a, &b, &c);
            a--;b--;

            G[a][b] = c;
            G[b][a] = c;

            E[i].u = a;
            E[i].v = b;
            E[i].w = c;
        }
        #ifdef DEBUG
        cout << "Read Graph " << (double)duration(timeNow()-t1)/1000000 << "ms" << endl;
        #endif
        #ifdef DEBUG
        setTime();
        #endif
        sum_visited = 0;
        visit(N, 0);
        if(testVisited(N)){
            continue;
        }
        #ifdef DEBUG
        cout << "Test Conectivity " << (double)duration(timeNow()-t1)/1000000 << "ms" << endl;
        #endif

        #ifdef DEBUG
        setTime();
        #endif
        kruskal(N, M);
        
        #ifdef DEBUG
        cout << "Kruskal: " << (double)duration(timeNow()-t1)/1000000 << "ms" << endl;
        #endif
        
    }
    return 0;
}
