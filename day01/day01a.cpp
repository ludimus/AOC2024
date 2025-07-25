#include <bits/stdc++.h>
#include <cmath>
using namespace std;
vector<int> A,B;



int main() {

    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int a,b;
    while (cin >> a >>b){
        A.push_back(a);
        B.push_back(b);
    }
    sort(A.begin(), A.end());
    sort(B.begin(), B.end());
    int total=0;
    for (int i=0;i<size(A);i++){
        total+=abs(A[i]-B[i]);
    }
    cout << total << endl;
    return 0;
}