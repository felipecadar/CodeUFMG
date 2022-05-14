#define DEBUG

#include <stdio.h>
#include <string.h>

#include <algorithm>
#include <iostream>
#include <queue>

#define MAX_N 101
#define INF 99999
using namespace std;

int dijkstra(int G[MAX_N][MAX_N], int N, int dist[MAX_N], int visited[MAX_N], int pred[MAX_N], int from, int to, int valid[MAX_N]) {
    memset(dist, INF, N);
    memset(pred, -1, N);
    memset(visited, 0, N);

    for (int i = 0; i < N; i++) {
        dist[i] = INF;
        pred[i] = -1;
        visited[i] = 0;
    }

    int u, v, d;
    dist[0] = 0;
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    pq.push(make_pair(from, 0));

    while (!pq.empty()) {
        d = pq.top().first;
        u = pq.top().second;
        pq.pop();

        if (visited[u] == 0) {
            visited[u] = 1;
            for (int v = 0; v < N; v++) {
                if (G[u][v] >= 0 && valid[v] == 1) {
                    if (dist[v] > dist[u] + G[u][v]) {
                        dist[v] = dist[u] + G[u][v];
                        pred[v] = u;
                        pq.push(make_pair(dist[v], v));
                    }
                }
            }
        }
    }

    return dist[to];
}

int main(int argc, char const *argv[]) {
    int N, M;
    int A, B, W;
    int C;

    int G[MAX_N][MAX_N];
    int dist[MAX_N];
    int pred[MAX_N];
    int valid[MAX_N];
    int visited[MAX_N];
    int inst = 0;

    while (scanf("%d %d", &N, &M) > 0) {
        memset(G, -1, MAX_N * MAX_N);

        printf("Instancia %d\n", ++inst);
        for (int i = 0; i < M; i++) {
            scanf("%d %d %d", &A, &B, &W);
            A--;
            B--;
            if (G[A][B] > -1) {
                G[A][B] = min(G[A][B], W);
            } else {
                G[A][B] = W;
            }
        }

        scanf("%d", &C);
        int FROM, TO, BY;
        for (int i = 0; i < C; i++) {
            memset(visited, 0, MAX_N);
            memset(valid, 0, MAX_N);

            scanf("%d %d %d", &FROM, &TO, &BY);

            FROM--;
            TO--;
            // BY--;
            if (BY == 0) {
                printf("[%d->%d] = %d\n", FROM, TO, G[FROM][TO]);
                cout << G[FROM][TO] << endl;
            } else {
                for (int j = 0; j < BY; j++) {
                    valid[j] = 1;
                }
                valid[FROM] = 1;
                valid[TO] = 1;
                for (int j = 0; j < N; j++)
                {
                    cout << valid[j] << " ";
                }
                cout << endl;
                
                printf("[%d->%d[%d]] = %d\n", FROM, TO, BY, G[FROM][TO]);

                int d = dijkstra(G, N, dist, visited, pred, FROM, TO, valid);
                if (d < INF) {
                    cout << d << endl;
                } else {
                    cout << -1 << endl;
                }
            }
        }

        printf("\n");
    }

    return 0;
}
