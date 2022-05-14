#define DEBUG

#include <iostream>
#include <string.h>
#include <limits.h>
#include <stdio.h>
#include <algorithm>
#include <queue>

#define MAX_N 110
#define MAX_M 20000
#define INF INT_MAX
using namespace std;

void BFS(int G[MAX_N][MAX_N], int N, int visited[MAX_N], int sorted[MAX_N], int &n_sorted){
    queue<int> q;
    int idx = 0;
    q.push(0);
    while (!q.empty())
    {
        int u = q.front();
        q.pop();

        // cout << "Dequeu: " << u << endl;
        for (int v = 0; v < N; v++)
        {
            if(G[u][v] > 0){
                if(visited[v] == 0){
                    q.push(v);
                    visited[v] = 1;
                    // cout << "Visited: " << v << endl; 
                }
            }
        }

        sorted[idx] = u;
        idx++;
    }
    n_sorted = idx;
    
    return;
}

void shortestPath(int G[MAX_N][MAX_N], int N, int sorted[MAX_N], int n_sorted, int pred[MAX_N], int dist[MAX_N]){
    for (int i = 0; i < n_sorted; i++)
    {   
        int u = sorted[i];
        for (int v = 0; v < N; v++)
        {
            if(G[u][v] > 0){
                // cout << u << "->" << v << " == " << G[u][v] << endl;
                if(dist[v] > dist[u] + G[u][v] || dist[v] == 0){

                    dist[v] = dist[u] + G[u][v];
                    pred[v] = u;
                }
            }
        }
    }
}

void stats(int N, int n_sorted, int sorted[MAX_N], int pred[MAX_N], int dist[MAX_N]){
        cout << "Sorted: ";
        for (int i = 0; i < n_sorted; i++)
        {
            cout << sorted[i] << " ";
        }
        cout << endl;
        
        cout << "Pred: ";
        for (int i = 0; i < N; i++)
        {
            cout << pred[i] << " ";
        }
        cout << endl;

        cout << "Dist: ";
        for (int i = 0; i < N; i++)
        {
            cout << dist[i] << " ";
        }
        cout << endl;
}

int main(int argc, char const *argv[])
{
    int N, M;
    int A, B, T, R;

    int Bus[MAX_N][MAX_N];
    int Plane[MAX_N][MAX_N];
    int sorted[MAX_N];
    int visited[MAX_N];
    int pred[MAX_N];
    int dist[MAX_N];
    int n_sorted;
    int valid_plane, valid_bus;

    while(scanf("%d %d", &N, &M) > 0){
        memset(Bus, 0, sizeof(Plane));
        memset(Plane, 0, sizeof(Plane));
        valid_plane = 0;
        valid_bus = 0;
        for (int i = 0; i < M; i++)
        {
            scanf("%d %d %d %d", &A, &B, &T, &R);

            if(T){
                Plane[--A][--B] = R;
                valid_plane = 1;
            }else{
                Bus[--A][--B] = R;
                valid_bus = 1;
            }
        }

        //Test fot bus;
        memset(pred, -1, sizeof(pred));
        memset(dist, 0, sizeof(dist));
        memset(visited, 0, sizeof(visited));
        memset(sorted, -1, sizeof(sorted));

        BFS(Bus, N, visited, sorted, n_sorted); // make topological sort
        if(visited[N-1] == 1){
            shortestPath(Bus, N, sorted, n_sorted, pred, dist);
        }else{
            valid_bus = 0;
        }
        int bus_dist = dist[N-1];
        // cout << "Bus dist: " << bus_dist << endl;
        // stats(N, n_sorted, sorted, pred, dist);

        // cout << endl;
        //Test fot plane;
        memset(pred, -1, sizeof(pred));
        memset(dist, 0, sizeof(dist));
        memset(visited, 0, sizeof(visited));
        memset(sorted, -1, sizeof(sorted));

        BFS(Plane, N, visited, sorted, n_sorted); // make topological sort
        if(visited[N-1] == 1){
            shortestPath(Plane, N, sorted, n_sorted, pred, dist);
        }else{
            valid_plane = 0;
        }
        int plane_dist = dist[N-1];
        // cout << "Plane dist: " << plane_dist << endl;
        // stats(N, n_sorted, sorted, pred, dist);
        
        if(valid_bus > 0 && valid_plane > 0){
            cout << min(plane_dist, bus_dist) << endl;
        }else{
            if(valid_bus > 0)
                cout << bus_dist << endl;
            if(valid_plane > 0)
                cout << plane_dist << endl;
        }

    }
    
    return 0;
}
