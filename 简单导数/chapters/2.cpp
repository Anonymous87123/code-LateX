#include <bits/stdc++.h>
using namespace std;
void solve() {
    int n;
    cin >> n;
    vector<vector<int>> blogs(n);
    for (int i = 0; i < n; ++i) {
        int l;
        cin >> l;
        vector<int> temp(l);
        for (int j = 0; j < l; ++j) cin >> temp[j];
        set<int> seen;
        for (int j = l - 1; j >= 0; --j) {
            if (seen.find(temp[j]) == seen.end()) {
                blogs[i].push_back(temp[j]);
                seen.insert(temp[j]);
            }
        }
    }
    vector<int> finalQ;
    vector<bool> used(n, false);
    set<int> gloseen;
    for (int i = 0; i < n; ++i) {
        int bestIdx = -1;
        vector<int> bestSuffix;
        for (int j = 0; j < n; ++j) {
            if (used[j]) continue;
            vector<int> cur;
            for (int x : blogs[j]) {
                if (gloseen.find(x) == gloseen.end()) {
                    cur.push_back(x);
                }
            }
            if (bestIdx == -1 || cur < bestSuffix) {
                bestSuffix = cur;
                bestIdx = j;
            }
        }
        used[bestIdx] = true;
        for (int x : bestSuffix) {
            finalQ.push_back(x);
            gloseen.insert(x);
        }
    }
    for (int i = 0; i < finalQ.size(); ++i) {
        cout << finalQ[i] << (i == finalQ.size() - 1 ? "" : " ");
    }
    cout << endl;
}
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}