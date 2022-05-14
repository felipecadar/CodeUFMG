#include <cstring>
#include <iostream>
#include <algorithm>    

#define MAXC 1100
#define MAXT 2100
using namespace std;
#define MAX(x, y) x > y ? x : y

int dp[MAXC][MAXT];
int size[MAXC];
int val[MAXC];
int N, T;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int c, v;

    while (cin >> N >> T) {
        memset(dp, -1, sizeof(dp));
        for (int i = 0; i < N; i++) {
            cin >> c >> v;
            size[i+1] = c;
            val[i+1] = v;
        }
        
        for (int i = 0; i <= N; i++) {
            for (int j = 0; j <= T; j++) {

                if (i == 0 || j == 0) {
                    dp[i][j] = 0;
                }

                if (size[i] > j) {
                    dp[i][j] = dp[i - 1][j];
                }

                if (size[i] <= j) {
                    int a1 = dp[i - 1][j];
                    int a2 = dp[i - 1][j - size[i]] + val[i];
                    int a3 = dp[i][j - size[i]] + val[i];

                    int m = max({a1, a2, a3});

                    dp[i][j] = m;
                }
            }
        }

        // for (int i = 1; i <= N; i++) {
        //     cout << "[" << size[i] << "," << val[i] << "] ";
        // }
        // cout << endl;

        // for (int i = 0; i <=N; i++) {
        //     for (int j = 0; j <= T; j++) {
        //         cout << dp[i][j] << " ";
        //     }
        //     cout << endl;
        // }
        cout << dp[N][T] << endl;
    }

    return 0;
}
