#include <iostream>
#include <cstring>
#include <algorithm>
#include <map>
#include <vector>

using namespace std;
#define MAXN 10000

long long int cards[MAXN];
long long int rounds[MAXN][2];
long long int N, c;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    while (cin >> N) {       
        for (long long int i = 0; i < N; i++)
        {
            cin >> cards[i];
        }

        for (long long int i = 0; i < N-1; i++)
        {
            rounds[i][0] = max(cards[i], cards[i+1]); //last round with interval=2
        }

        // cout << "[INIT]" << endl;
        // for(long long int ii = 0; ii < N; ii++){
        //     cout << rounds[ii][0] << " ";
        // }
        // cout << endl;
        // for(long long int ii = 0; ii < N; ii++){
        //     cout << rounds[ii][1] << " ";
        // }
        // cout << endl;

        long long int turn = 1;
        long long int opt1, opt2;
        for(long long int n=4; n <= N; n+=2){
            for(long long int i=0; i+n <= N; i++){
                long long int end = i + n - 1;


                opt1 = cards[i] + min(rounds[i+1][1-turn], rounds[i+2][1-turn]); // Alberto choose card at the init and Wanderlay choose que best for min in prev round
                opt2 = cards[end] + min(rounds[i][1-turn], rounds[i+1][1-turn]); // Alberto choose card at the end and Wanderlay choose que best for min in prev round

                rounds[i][turn] = max(opt1, opt2);

                // cout << "[" << i << "," << end << "]" << endl;
                // for(long long int ii = 0; ii < N; ii++){
                //     cout << rounds[ii][0] << " ";
                // }
                // cout << endl;
                // for(long long int ii = 0; ii < N; ii++){
                //     cout << rounds[ii][1] << " ";
                // }
                // cout << endl;


            }
            turn = 1-turn; // flip memory
        }

        cout << rounds[0][1-turn] << endl;

    }
    return 0;
}