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

int dijkstra(int G[MAX_N][MAX_N], int N, int dist[MAX_N], int visited[MAX_N], int pred[MAX_N]){
    for (int i = 0; i < N; i++)
    {
        dist[i] = INF;
        pred[i] = -1;
        visited[i] = 0;
    }

    int u, v, d;
    dist[0] = 0;
    priority_queue< pair<int,int>, vector <pair<int,int>> , greater<pair<int,int>> > pq;
    pq.push(make_pair(0,0));

    while(!pq.empty()){
        d = pq.top().first;
        u = pq.top().second;
        pq.pop();

        if(!visited[u]){
            visited[u] = 1;
            for (int v = 0; v < N; v++)
            {
                if(G[u][v] > 0){
                    if(dist[v] > dist[u] + G[u][v]){
                        dist[v] = dist[u] + G[u][v];
                        pred[v] = u;
                        pq.push(make_pair(dist[v], v));
                    }
                }
            }
            
        }

    }

    return dist[N-1];
}

int main(int argc, char const *argv[])
{
    int N, M;
    int A, B, T, R;

    int Bus[MAX_N][MAX_N];
    int Plane[MAX_N][MAX_N];
    int visited[MAX_N];
    int pred[MAX_N];
    int dist[MAX_N];
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
        int bus_dist = dijkstra(Bus, N, dist, visited, pred);
        int plane_dist = dijkstra(Plane, N, dist, visited, pred);

        cout << min(plane_dist, bus_dist) << endl;
    }
    
    return 0;
}
