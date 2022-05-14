#include <iostream>
#include <cstring>
#define MAXR 200
#define MAXK ((MAXR * (MAXR-1)) / 2)

using namespace std;

bool dp[MAXR][MAXK];
int degree[MAXR];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int R, K, u, v;
    while (cin >> R >> K) {
        // memset(dp, 0, sizeof(bool)*R*K);
        memset(degree, 0, sizeof(degree));
        
        for (int i = 0; i < K; i++)
        {   
            cin >> u >> v;
            u--;v--;
            degree[u]++;
            degree[v]++;

        }
        for (int i = 1; i <= R; i++)
        {
            dp[i][0] = 1;
            for (int j = 1; j <= K; j++)
            {
                dp[i][j] = dp[i-1][j];
                if (degree[i-1] <= j){
                    dp[i][j] += dp[i-1][j-degree[i-1]]; 
                }
            }
        }
        
        if(dp[R][K]){
            cout << "S" << endl;
        }
        else{
            cout << "N" << endl;
        }

    }
    return 0;
}