#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;
void solve() {
    int n;cin >> n;
    string s;cin >> s;
    vector<long long> p2(n + 1, 1);
    for (int i = 1; i <= n; i++) {
        p2[i] = (p2[i - 1] * 2) % MOD;
    }
    long long left = 0;
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') {
            left = (left + p2[i]) % MOD;
        }
    }
    long long prod = 1;
    int l1_right = 0;
    int p = 0;
    vector<int> current;
    bool in_E = false;
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') {
            p++;
            if (p == 2 && !in_E) {
                in_E = true;
                current.clear();
            }
            if (in_E) {
                current.push_back(1);
            }
        } else {
            p--;
            if (in_E) {
                current.push_back(0);
                if (p == 1) { 
                    in_E = false;
                    long long sum_left = 0;
                    int sz = current.size();
                    for (int k = 0; k < sz; k++) {
                        if (current[k] == 1) {
                            sum_left = (sum_left + p2[k]) % MOD;
                        }
                    }
                    long long w = (p2[sz] - sum_left + MOD) % MOD;
                    prod = (prod * w) % MOD;
                }
            } else if (p == 0) {
                l1_right++;
            }
        }
    }
    prod = (prod * p2[l1_right]) % MOD;
    prod = (prod - 1 + MOD) % MOD;
    long long total = (left + prod) % MOD;
    cout << total << "\n";
}
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    int t;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    return 0;
}