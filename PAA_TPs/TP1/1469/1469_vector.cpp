#include <iostream>
#include <vector>
#include <queue>
using namespace std;

typedef vector<vector<int> > graph;
typedef vector<int> veci;

void printG(graph G){
    for (int i = 0; i < G.size(); i++)
    {
        cout << "[" << i << "] ";
        for (int j = 0; j < G[i].size(); j++)
        {
            cout << G[i][j] << " ";
        }
        cout << endl;
    }
    
}

void change(graph &G, int arg1, int arg2){
    for (int i = 0; i < G.size(); i++)
    {
        // if(i == arg1 || i == arg2){continue;}
        for (int j = 0; j < G[i].size(); j++)
        {
            if(G[i][j] == arg1){
                G[i][j] = arg2;
            }
            else{
                if(G[i][j] == arg2){
                    G[i][j] = arg1;
                }
            }
        }
    }
    swap(G[arg1], G[arg2]);
    // veci tmp = G[arg1];
    // G[arg1] = G[arg2];
    // G[arg2] = tmp;
}

void backprop(graph G, veci K, int search, int &min_age, veci &passed){
    // cout << "N(" << search << ") -> " << G[search].size() << "-" << passed[search] << endl;
    if(passed[search] == 1){return;}
    for (int i = 0; i < G[search].size(); i++)
    {
        if(min_age == 0 || min_age > K[G[search][i]]){
            min_age = K[G[search][i]];
        }
        if(passed[G[search][i]] == 0){
            backprop(G, K, G[search][i], min_age, passed);
        }
        
    }
    passed[search] = 1;
}


int main(int argc, char const *argv[])
{   
        int N, M, I, x, y, k;
        graph G;
        veci K;
        veci passed;
        while(scanf("%i %i %i", &N, &M, &I) > 0){
            for (int i = 0; i < N; i++)
            {
                scanf("%i", &k);
                K.push_back(k);
                passed.push_back(0);
            }
            G.assign(N, veci());
            
            for (int i = 0; i < M; i++)
            {
                scanf("%i %i", &x, &y);
                x--;y--;
                G[y].push_back(x);
            }
            // printG(G, N);

            // printG(G, N);
            // Intructions

            for (int i = 0; i < I; i++)
            {   
                char opt[2];
                int arg1, arg2;
                scanf("%s", opt);

                if(opt[0] == 'P'){
                    scanf("%i", &arg1);
                    int min = 0;
                    // cout << "--------->P " << arg1-1<< "-> ";
                    fill(passed.begin(), passed.end(), 0);
                    backprop(G, K, arg1-1, min, passed);
                    if(min > 0){
                        cout << min << endl;
                    }else{
                        cout << "*" << endl;
                    }
                }
                if(opt[0] == 'T'){
                    scanf("%i %i", &arg1, &arg2);
                    arg1--; arg2--;
                    // cout << "T " << arg1 << " " << arg2 << endl;
                    // printG(G);
                    change(G, arg1, arg2);
                    // cout << "------------" << endl;
                    // printG(G);
                }
            }
            
        }
    return 0;
}
