#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include<vector>
#include <queue>
// #include<bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<int, int> pii;
const ll inf = (ll)1e16;

vector <pii> V[270000+10];
bool vis[270000+10];
ll dis[270000+10];
ll dis1[270000+10];

int route[270000+10];
vector<pii> del_path;
struct Node{
	int id;
	ll d;
	Node(){}
	Node(int id, ll d):id(id),d(d){}
	bool operator < (const Node &A)const{
		return d > A.d;
	}
};

void dijkstra(int st,int n){
	for(int i=1; i<=n; i++){
		vis[i] = 0;
		dis[i] = inf;
	}
	dis[st] = 0;
	priority_queue<Node> Q;
	Q.push(Node(st, 0));
	Node nd;

	while(!Q.empty()){
		nd = Q.top(); Q.pop();
		if(vis[nd.id]) continue;
		vis[nd.id] = true;
		for(int i=0; i<V[nd.id].size(); i++){
			int j = V[nd.id][i].first;
			int k = V[nd.id][i].second;
			if(nd.d + k <dis[j] && !vis[j]){
                    dis[j] = nd.d + k;
                    route[j]=nd.id;
                    Q.push(Node(j, dis[j]));
            }
		}
	}
	
}



void reverse_dijkstra(int st,int n){
	for(int i=1; i<=n; i++){
		vis[i] = 0;
		dis1[i] = inf;
	}

	dis1[st] = 0;
	priority_queue<Node> Q;
	Q.push(Node(st, 0));
	Node nd;

	while(!Q.empty()){
		nd = Q.top(); Q.pop();
		if(vis[nd.id]) continue;
		vis[nd.id] = true;
		for(int i=0; i<V[nd.id].size(); i++){
			int j = V[nd.id][i].first;
			int k = V[nd.id][i].second;
			if(nd.d + k <dis1[j] && !vis[j]){
                    dis1[j] = nd.d + k;
                    Q.push(Node(j, dis[j]));
                
			}
		}
	}
}
int current_min;
vector<pii> used_edge;

void init_reverse(int e,int n){
    current_min=int(dis[e]);
    used_edge.clear();
    reverse_dijkstra(e,n);
    int st=e;
    while(route[st]!=0){
        used_edge.push_back(make_pair(route[st],st));
        st=route[st];
    }
}
int route1[270000+10];
void get_next_shortest_path(int n){
    int MIN=1000000000;
    int au=-1;
    int av=-1;
    for(int _id=1;_id<=n;_id++){
        for(int i=0; i<V[_id].size(); i++){
			int j = V[_id][i].first;
			int k = V[_id][i].second;
            bool used=false;
            for(int up=0;up<used_edge.size();up++){
                int u=used_edge[up].first;
                int v=used_edge[up].second;
                if(u==_id&&v==j){
                    used=true;
                    break;
                }
            }
            if(used){
                continue;
            }
            if(dis[_id]+dis1[j]+k-current_min<=MIN){
                au=_id;
                av=j;
                MIN=dis[_id]+dis1[j]+k-current_min;
            }
        }
    }
    current_min=MIN+current_min;
    used_edge.push_back(make_pair(au,av));
    for(int i=1;i<=n;i++){
        route1[i]=route[i];
    }
    route1[av]=au;
    

}

void init(int n){
    del_path.clear();
    for(int i=1;i<=n;i++){
        V[i].clear();
    }
    memset(route,0,sizeof(route));
}

void add_del_path(int x,int y){
    del_path.push_back(make_pair(x, y));
}

void add_edge(int x,int y,int z){
    V[x].push_back(make_pair(y, z));
}
void run_dijkstra(int st,int n){
    dijkstra(st,n);
}

int get_shortest_path(int e){
    return int(dis[e]);
}
int get_current_shortest_path_length(){
    return current_min;
}
int get_current_route(int x){
    return route1[x];
}
int get_route(int x){
    return route[x];
}


PYBIND11_MODULE(dijkstra, m) {
    m.doc() = "pybind11 dijkstra plugin"; // optional module docstring
    
    // m.def("add", &add, "A function which adds two numbers");
    m.def("init", &init, "init");
    m.def("add_edge", &add_edge, "add_edge");
    m.def("run_dijkstra", &run_dijkstra, "run_dijkstra");
    m.def("get_shortest_path", &get_shortest_path, "get_shortest_path");
    m.def("get_route", &get_route, "get_route");
    
    m.def("add_del_path", &add_del_path, "add_del_path");

    m.def("init_reverse", &init_reverse, "init_reverse");
    m.def("get_next_shortest_path", &get_next_shortest_path, "get_next_shortest_path");
    m.def("get_current_shortest_path_length", &get_current_shortest_path_length, "get_current_shortest_path_length");
    m.def("get_current_route", &get_current_route, "get_current_route");



    // m.def("get_up", &get_up, "get_up");


}

// int main(){
// 	int x, y, z, st, ed, cas = 0;
// 	scanf("%d", &cas);
// 	while(cas--){
// 		scanf("%d%d%d", &n, &m, &st);
// 		for(int i=1; i<=n; i++) V[i].clear();
// 		while(m--){
// 			scanf("%d%d%d", &x, &y, &z);
// 			V[x].push_back(make_pair(y, z));
// 			//V[y].push_back(make_pair(x, z));
// 		}
		
// 		for(int i=1; i<=n; i++)
// 			if(i==1) printf("%d", dis[i]);
// 			else printf(" %d", dis[i]);
// 	}
// }
