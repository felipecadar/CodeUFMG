#include <map>
#include <cstring>
#include <iostream>
#define limit 1000000
using namespace std;
typedef unsigned long long ull;

// ull memory[limit];
std::map<ull, ull> memory;

ull divide(ull n, ull k, ull l) {
    if (n <= 0)
        return 1;
    if (n == 1)
        return k % limit;
    if (n == 2)
        return ((k * k) % limit + l) % limit;
    if (n == 3)
        return (((((k * k) % limit) * k) % limit) + ((k * l) % limit) + ((l * k) % limit)) % limit;

    if (memory.find(n) != memory.end())
        return memory[n];

    ull aux1, aux2, aux3, aux4;
    ull t1, t2, t3;
    ull r;

    if (n % 2 == 0) {
        ull mid = n / 2;
        t1 = divide(mid, k, l);
        t2 = divide(mid - 1, k, l);
        aux1 = (t1 * t1) % limit;
        aux2 = (((t2 * t2) % limit) * l) % limit;
        r = (aux1 + aux2) % limit;
    } else {
        ull mid = (n - 1) / 2;
        t1 = divide(mid, k, l);
        t2 = divide(mid - 1, k, l);
        t3 = divide(mid - 2, k, l);

        aux1 = (((t1 * t1) % limit) * k) % limit;
        aux2 = (((t2 * t2) % limit) * ((l * k) % limit)) % limit;
        aux3 = (((t1 * t2) % limit) * l) % limit;
        aux4 = (((t2 * t3) % limit) * ((l * l) % limit)) % limit;
        r = (aux1 + aux2 + aux3 + aux4) % limit;
    }
    memory[n] = r;
    return r;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    ull n, k, l;
    ull S;

    while (cin >> n >> k >> l) {
        n = n / 5;
        memory.clear();

        // n = n%limit;
        k = k % limit;
        l = l % limit;

        S = divide(n, k, l);

        printf("%06llu\n", S);
    }
    return 0;
}