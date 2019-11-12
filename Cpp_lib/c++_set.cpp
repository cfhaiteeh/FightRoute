#include <pybind11/pybind11.h>
#include <set>
#include <pybind11/stl.h>
std::set<int> S[2][800];

void init(int n){
    for(int i=0;i<n;i++){
        S[0][i].clear();
        S[1][i].clear();
        S[0][i].insert(100000000);
        S[1][i].insert(1);
    }
}
void insert(int id,int v) {
   S[0][id].insert(v);
   S[1][id].insert(-v);
}


int get_low(int id,int v){
    int val=*S[1][id].upper_bound(-v);
    return -val;
}
int get_up(int id,int v){
    int val=*S[0][id].upper_bound(v);
    return val;
}

PYBIND11_MODULE(cpp_set, m) {
    m.doc() = "pybind11 cpp_set plugin"; // optional module docstring
    
    // m.def("add", &add, "A function which adds two numbers");
    m.def("init", &init, "init");
    m.def("insert", &insert, "insert");
    m.def("get_low", &get_low, "get_low");
    m.def("get_up", &get_up, "get_up");


}