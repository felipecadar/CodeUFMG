#include <iostream>
#include <string>
#include <vector>

using namespace std;

void printStack(vector<int> res) {
    for (int i = 0; i < res.size(); i++) {
        cout << res[i];
    }
    cout << endl;
}

int main() {
    int N, D;
    int c;
    int del, top;
    char num[100100];
    while (true) {
        scanf("%d %d", &N, &D);
        c = scanf("%s", num);
        if (c < 0) break;
        vector<int> res;
        del = 0;
        // printStack(res);
        for (int i = 0; i < N; i++) {
            c = (int)(num[i] - '0');

            while (!res.empty() && del < D && c > res.back()) {
                res.pop_back();
                del++;
            }

            // if(del == D) break;

            res.push_back(c);
        }
        for (int i = 0; i < N-D; i++) {
            cout << res[i];
        }
        cout << endl;
    }

    return 0;
}
