#include <map>
#include <cstring>
#include <iostream>
#include <vector>
#include <algorithm>

#define limit 1000
using namespace std;
typedef unsigned long long ull;
#define min(x,y) x > y ? y : x
#define D(x) cout << #x " = " << (x) << endl


map<int, int> memory;
int tryPatch(int init, int t1, int t2, vector<int> distances){
    int end = distances.size();
    if(init==end){
        int m = min(t1, t2);
        return m;
    }
    if(init > end)
        return 0;

    if(memory.find(init)!= memory.end())
        return memory[init];

    //try patch 1
    int len = t1;
    int i = init;
    while(len >= 0 && i < end){
        len -= distances[i]; //try to consume the hole patch
        i++; // next hole
    }
    if(i == end)
        i++; // hole i is covered

    //try patch 1
    len = t2;
    int j = init;
    while(len >= 0 && j < end){
        len -= distances[j];
        j++; 
    }
    if(j == end)
        j++; // hole i is covered

    int usingt1 = t1+tryPatch(i, t1, t2, distances);
    int usingt2 = t2+tryPatch(j, t1, t2, distances);

    memory[init] = min(usingt1, usingt2);
        
    // cout << "[" << init << "," << end << "] == " << memory[init] << endl;

    return memory[init];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N, C, T1, T2;
    int holes[1000];

    vector<int> distances;
    vector<int> distances_sorted;
    while (cin >> N >> C >> T1 >> T2)
    {   
        distances.clear();
        distances_sorted.clear();
        memory.clear();

        for (int i = 0; i < N; i++)
        {
            cin >> holes[i];
        }

        for (int i = 0; i < N-1; i++)
        {
            distances.push_back(holes[i+1] - holes[i]);
        }
        distances.push_back(holes[0] - holes[N-1] + C); //last hole to the first
        int max = max_element(distances.begin(), distances.end()) - distances.begin(); 

        for(int i = max+1; i < N; i++)
            distances_sorted.push_back(distances[i]);

        for(int i = 0; i < max+1; i++)
            distances_sorted.push_back(distances[i]);


        // cout << "t1 = " << T1 << " T2 = " << T2 << endl;
        // for (int i = 0; i < N; i++)
        // {
        //     cout << distances[i] << " ";
        // }
        // cout << endl;
        // for (int i = 0; i < N; i++)
        // {
        //     cout << distances_sorted[i] << " ";
        // }
        // cout << endl;

        int total = tryPatch(0, T1, T2, distances_sorted);
        
        cout << total << endl;

    }
    

    return 0;
}


