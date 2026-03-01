#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll NEG = (ll)-4e18;
struct BITMax {
    int n;
    vector<ll> bit;
    BITMax(int n=0){init(n);}
    void init(int n_) {
        n = n_;
        bit.assign(n+1, NEG);
    }
    void update(int idx, ll val) {
        for (; idx <= n; idx += idx & -idx)
            bit[idx] = max(bit[idx], val);
    }
    ll query(int idx) {
        ll res = NEG;
        for (; idx > 0; idx -= idx & -idx)
            res = max(res, bit[idx]);
        return res;
    }
};
struct Query {
    ll x;
    int ylimit;
    int id;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    cin >> t;
    while (t--) {
        int n, m;
        cin >> n >> m;
        vector<vector<ll>> bucket(n+1); 
        for (int i = 0; i < n; i++) {
            ll x; int y;
            cin >> x >> y;
            bucket[y].push_back(x);
        }
        int Kmax = n + 1;
        vector<int> cnt(Kmax+1, 0);
        vector<ll> top(Kmax+1, NEG), kth(Kmax+1, 0), allsum(Kmax+1, 0);
        multiset<ll> big, small;
        ll sumBig = 0;
        ll sumAll = 0;
        int total = 0;
        auto move = [&]() {
            auto it = prev(small.end());
            ll v = *it;
            small.erase(it);
            big.insert(v);
            sumBig += v;
        };
        auto moveb = [&]() {
            auto it = big.begin();
            ll v = *it;
            big.erase(it);
            sumBig -= v;
            small.insert(v);
        };
        auto addValue = [&](ll v, int K) {
            total++;
            sumAll += v;
            if ((int)big.size() < K) {
                big.insert(v);
                sumBig += v;
            } else {
                if (!big.empty()) {
                    ll minBig = *big.begin();
                    if (v > minBig) {
                        moveb();
                        big.insert(v);
                        sumBig += v;
                    } else {
                        small.insert(v);
                    }
                } else {
                    small.insert(v);
                }
            }
            while ((int)big.size() < K && !small.empty()) move();
            while ((int)big.size() > K) moveb();
        };
        for (int tthr = n; tthr >= 0; --tthr) {
            int K = tthr + 1; 
            for (ll v : bucket[tthr]) addValue(v, K);
            while ((int)big.size() > K) moveb();
            while ((int)big.size() < K && !small.empty()) move();
            cnt[K] = total;
            allsum[K] = sumAll;
            if (cnt[K] >= K && (int)big.size() == K) {
                top[K] = sumBig;
                kth[K] = *big.begin(); 
            } else {
                top[K] = NEG;
                kth[K] = 0;
            }
        }
        vector<ll> prefTop(Kmax+1, NEG);
        vector<ll> prefMiss(Kmax+1, NEG);
        for (int k = 1; k <= Kmax; k++) {
            prefTop[k] = max(prefTop[k-1], top[k]);
            if (cnt[k] == k-1) prefMiss[k] = max(prefMiss[k-1], allsum[k]);
            else prefMiss[k] = prefMiss[k-1];
        }
        ll baseBest = prefTop[Kmax];
        if (baseBest < 0) baseBest = 0;
        struct Entry { ll key; int pos; ll val; };
        vector<Entry> entries;
        entries.reserve(Kmax);
        for (int k = 1; k <= Kmax; k++) {
            if (top[k] != NEG) {
                entries.push_back({kth[k], k, top[k] - kth[k]});
            }
        }
        sort(entries.begin(), entries.end(), [](const Entry& a, const Entry& b){
            return a.key < b.key;
        });
        vector<Query> qs(m);
        for (int i = 0; i < m; i++) {
            ll x; int y;
            cin >> x >> y;
            int Y = min(Kmax, y + 1);
            qs[i] = {x, Y, i};
        }
        vector<int> order(m);
        iota(order.begin(), order.end(), 0);
        sort(order.begin(), order.end(), [&](int a, int b){
            return qs[a].x < qs[b].x;
        });
        BITMax bit(Kmax);
        int p = 0;
        vector<ll> ans(m, 0);
        for (int idx : order) {
            ll x = qs[idx].x;
            int Y = qs[idx].ylimit;
            while (p < (int)entries.size() && entries[p].key < x) {
                bit.update(entries[p].pos, entries[p].val);
                p++;
            }
            ll best = baseBest;
            best = max(best, prefTop[Y]);
            if (prefMiss[Y] != NEG) best = max(best, prefMiss[Y] + x);
            ll b = bit.query(Y);
            if (b != NEG) best = max(best, b + x);
            ans[qs[idx].id] = best;
        }
        for (int i = 0; i < m; i++) {
            cout << ans[i] << (i+1==m? '\n' : ' ');
        }
    }
    return 0;
}
