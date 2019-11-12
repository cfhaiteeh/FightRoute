# -*- coding: utf-8 -*-
import numpy as np
import sys
import Cpp_lib.cpp_set as c_set
import Cpp_lib.dijkstra as dijkstra
from time import *
sys.setrecursionlimit(1000000)
class Model():
    """ Encodes an input sequence. """
    def __init__(self, csv_data,args):
        super().__init__()

        self.csv_data=csv_data
        self.len=len(csv_data)
        self.prob=args.prob
        self.c_set=c_set
        self.c_set.init(self.len)
        self.fa=[]
        self.now=[]
        self.dist_data=self.get_dist()
        self.max_dis=max(args.alpha1,args.alpha2,args.beta1,args.beta2)*1000+100
        self.ans=np.full((self.len+10,self.max_dis),10000000)
        self.delta=int(args.delta*1000)
        #垂直
        self.alpha=[int(args.alpha1*1000),int(args.alpha2*1000)]
        #水平
        # self.allow=[]
        self.beta=[int(args.beta1*1000),int(args.beta2*1000)]
        self.thet=int(args.thet*1000)
        self.vis=np.full((self.len+10,self.max_dis),0)
        # self.all=np.full((350,30000),0)
        self.d_inf=10000000.0
        self.inf=10000000
        # self.UNK=20000000
        self.d_zero=0.0
        self.zero=0
        self.error_pair=(self.inf,self.inf)
        self.val2id=np.full((self.len+10,self.max_dis),-1)
        self.max_point=args.max_point
        self.id2val=np.full( self.max_point,-1)
        # self.vis_all=np.full((self.len+10,self.max_dis),0)
        self.route=np.full((self.len+10,self.max_dis),-1)
        self.next=np.full((self.len+10,self.max_dis),0)
        # self.is_add=np.full((262992,262992),0)
        self.is_add=[]
        for i in range( self.max_point):
            self.is_add.append(dict())
        self.dijkstra=dijkstra
        self.dijkstra.init( self.max_point)

        self.s_id=2
        self.e_num=0
        self.point_num=0
        self.e_id=-1
        self.get_net_dijkstra()

    def get_dist(self):
        dist=np.full((self.len,self.len),-1)
        for i in range(self.len):
            dist[i][i]=0
            for j in range(i+1,self.len):
                x_c=self.csv_data[i][1]-self.csv_data[j][1]
                y_c=self.csv_data[i][2]-self.csv_data[j][2]
                z_c=self.csv_data[i][3]-self.csv_data[j][3]
                d=(x_c**2+y_c**2+z_c**2)**0.5
                dist[i][j]=dist[j][i]=int(d)
        return dist

    def allow_destination(self,vertical_val,horizontal_val,now_id):
        if  (self.csv_data[now_id][4]==0 ):
            if vertical_val > self.beta[0] or horizontal_val > self.beta[1]:
                return False
        if  (self.csv_data[now_id][4]==1 ):
            if  vertical_val>self.alpha[0] or  horizontal_val>self.alpha[1]:
                return False
        return True

    def get_ans(self,now_id,vertical_val,horizontal_val):

        if now_id==self.len-1:
            if  (vertical_val >self.thet or horizontal_val > self.thet):
                return -1, -1
            else:
                if self.vis[now_id][0] == 1:
                    return 1, 0
                self.vis[now_id][0]=1
                self.point_num += 1
                self.val2id[now_id][0] = self.s_id
                self.id2val[self.s_id]=now_id
                self.e_id=self.s_id
                self.s_id += 1
                return 1,0

        if self.allow_destination(vertical_val,horizontal_val,now_id) ^ 1:
            return -1,self.inf
        val = vertical_val
        if self.csv_data[now_id][4] == 1:
            val = horizontal_val
        if self.vis[now_id][val] == 1:
            return 1,val
        self.vis[now_id][val] = 1
        self.point_num+=1
        self.val2id[now_id][val]=self.s_id
        self.id2val[self.s_id] = now_id
        self.s_id+=1
        add=0
        if self.prob and self.csv_data[now_id][5]==1:
            add=5000

        for i in range(1,self.len):
            if i == now_id  :
                continue
            loss=(self.dist_data[now_id][i]*self.delta)
            if self.csv_data[now_id][4] == 1:
                  # tmp=min_dist
                  is_ok,_val=self.get_ans(i,loss+add,val+loss)
                  if is_ok!=-1:

                      u = self.val2id[now_id][val]
                      v = self.val2id[i][_val]


                      if (v in self.is_add[u])==0:
                          self.is_add[u][v]=1
                          self.e_num+=1
                          self.dijkstra.add_edge(u,v,self.dist_data[now_id][i])
            elif self.csv_data[now_id][4]==0:
                  # tmp=min_dist
                  is_ok,_val=self.get_ans(i,val+loss,loss+add)
                  if is_ok != -1:
                      u = self.val2id[now_id][val]
                      v = self.val2id[i][_val]
                      # print(u,v)
                      if (v in self.is_add[u])==0:
                          self.is_add[u][v] =1
                          self.e_num+=1
                          self.dijkstra.add_edge(u,v,self.dist_data[now_id][i])

        return 1,val

    def get_net_dijkstra(self):
        print('running raw model')
        print('data_len', self.len)
        start_val = -1
        self.val2id[0][0] = 1
        self.id2val[1] = 0

        for i in range(1, self.len):
            loss = self.dist_data[0][i] * self.delta
            is_ok, _v = self.get_ans(i, loss, loss)
            if (is_ok != -1):
                u = self.val2id[0][0]
                v = self.val2id[i][loss]
                if (v in self.is_add[u]) == 0:
                    self.is_add[u][v] = 1
                    self.e_num += 1
                    self.dijkstra.add_edge(u, v, self.dist_data[0][i])
        print('pn',self.point_num)
        print('en',self.e_num)
        print('s_id',self.s_id)
        print('e_id',self.e_id)
        next_id = 0
        next_val = start_val
        ans_route = []
        while (self.route[next_id][next_val] != -1):
            ans_route.append(next_id)
            x = self.route[next_id][next_val]
            y = self.next[next_id][next_val]
            next_id = x
            next_val = y
        ans_route.append(next_id)
        begin_time = time()
        self.dijkstra.run_dijkstra(1,  self.max_point)
        end_time = time()
        run_time = end_time - begin_time
        #
        print('dijkstra运行时间：', run_time)

    def run_raw(self):
        ans_min=self.dijkstra.get_shortest_path(self.e_id)

        ans_route = []
        pre = self.e_id
        while (True):
            n_id = self.id2val[pre]
            ans_route.append(n_id)
            pre = self.dijkstra.get_route(pre)
            if pre == 0:
                break

        print('ans_min=', ans_min)
        print('len=',len(ans_route[::-1]))
        print(ans_route[::-1])
        return ans_route[::-1]

    def run_angle(self):
        print('running angle model')
        print('data_len', self.len)
        self.dijkstra.init_reverse(self.e_id,  self.max_point)
        for i in range(4):
            self.dijkstra.get_next_shortest_path( self.max_point)
            ans_min = (self.dijkstra.get_current_shortest_path_length())
            ans_route = []
            pre = self.e_id
            while (True):
                # print(e)
                n_id = self.id2val[pre]
                # print(pre,n_id)
                # print(pre)
                ans_route.append(n_id)
                pre = self.dijkstra.get_current_route(pre)

                if pre == 0:
                    break
            print('ans_min=', ans_min)
            print(ans_route[::-1])

        return ans_route[::-1]





