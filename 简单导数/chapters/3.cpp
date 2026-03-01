#include <bits/stdc++.h>
using namespace std;
vector<int> get(int n, const vector<int>& a) {
    vector<int> dp_len(n);
    vector<int> tails; 
    for (int i = 0; i < n; ++i) {
        auto it = lower_bound(tails.begin(), tails.end(), a[i], greater<int>());
        if (it == tails.end()) {
            tails.push_back(a[i]);
            dp_len[i] = tails.size();
        } else {
            *it = a[i];
            dp_len[i] = distance(tails.begin(), it) + 1;
        }
    }
    return dp_len;
}
void solve() {
    int n;
    if (!(cin >> n)) return;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    vector<int> L = get(n, a);
    reverse(a.begin(), a.end());
    vector<int> R = get(n, a);
    reverse(R.begin(), R.end());

    int max_keep = 0;
    for (int i = 0; i < n; ++i) {
        max_keep = max(max_keep, L[i] + R[i] - 1);
    }
    cout << n - max_keep << "\n";
}
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}