#include <iostream>
#include <string.h>
#include <queue>
#define MAX_N 1000
using namespace std;

int G[MAX_N][MAX_N];
int visited[MAX_N];
int key[MAX_N];
int parent[MAX_N];

void visit(int N, int i){
    for (int j = 0; j < N; j++)
    {
        if (G[j][i] > 0 && visited[j] == 0){
            visited[j] = 1;
            visit(N, j);
        }
    }
}

int testVisited(int N){
    for (int i = 0; i < N; i++)
    {
        if(visited[i] == 0){
            cout << "impossivel" << endl;
            return 1;
        }
    }
    return 0;
}

void prim(int N){

    priority_queue<pair<int, int>, vector<pair<int, int>>, less<pair<int, int>>> pq; // pair <w, v>
    memset(key, -1, sizeof(key));
    memset(visited, 0, sizeof(visited));
    memset(parent, 0, sizeof(parent));

    int root = 0;
    int w = 0;
    pq.push(make_pair(w, root));
    key[root] = w;
    int max_w = w;

    while(!pq.empty()){

        int u = pq.top().second;
        pq.pop();

        if(visited[u])
            continue;

        visited[u] = 1;

        for (int n = 0; n < N; n++)
        {
            if(G[u][n] > 0){
                w = G[u][n];

                if(visited[n] == 0 && (key[n] > w || key[n] == -1)){
                    key[n] = w;
                    pq.push(make_pair(w, n));
                    parent[n] = u;
                    max_w = max(max_w, w);
                }

            }
        }
        
    }

    cout << max_w << endl;
}

int main(int argc, char const *argv[])
{
    int N,M;
    int a, b, c;
    while(cin >> N >> M){
        memset(G, 0, sizeof(G));
        memset(visited, 0, sizeof(visited));

        for (int i = 0; i < M; i++)
        {
            cin >> a >> b >>c;
            a--;b--;
            G[a][b] = c;
            G[b][a] = c;
        }

        visit(N, 0);
        if(testVisited(N)){
            continue;
        }

        prim(N);
        

        
    }
    return 0;
}
