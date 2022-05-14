#include <cstring>
#include <iostream>
#include <algorithm>
#define MAXC 1100
#define MAXT 2100
using namespace std;

int dp[MAXC][MAXT];
int size[MAXC];
int val[MAXC];
int N, T;

int Proft(int i, int j) {

    if (i == 0 || j == 0) {
        dp[i][j] = 0;
        return 0;
    }

    if (dp[i][j] != -1)
        return dp[i][j];

    if (size[i] > j){
        dp[i][j] = Proft(i - 1, j);
    }

    if (size[i] == j){
        dp[i][j] = max({Proft(i - 1, j), val[i]});
    }
    
    if(size[i] < j){
        dp[i][j] = max({Proft(i - 1, j), Proft(i - 1, j - size[i]) + val[i], Proft(i, j - size[i]) + val[i]});
    }

    return dp[i][j];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int c, v;

    while (cin >> N >> T) {
        memset(dp, -1, sizeof(dp));

        for (int i = 0; i < N; i++) {
            cin >> c >> v;
            size[i + 1] = c;
            val[i + 1] = v;
        }
        cout << Proft(N, T) << endl;

        // for (int i = 0; i < N; i++) {
        //     cout << "[" << size[i+1] << "," << val[i+1] << "] ";
        // }
        // cout << endl;

        
        // for (int i = 0; i < N; i++) {
        //     for (int j = 0; j < T; j++) {
        //         cout << dp[i][j] << " ";
        //     }
        //     cout << endl;
        // }
    }

    return 0;
}
