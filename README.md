# 多约束条件下智能飞行器航迹快速规划代码
代码实现了全部题目，并用pybind11实现了python与C++的无缝衔接。C++代码和库在Cpp_lib中。
#项目说明
- 第一问主要用记忆化深度优先搜索和dijkstra+堆优化实现
- 第二问在第一问的基础上，修正五条最短路径然后取最优航迹
- 第三问在第一题的基础上，设问题校正点出发时的误差变为5

### 代码运行
```
python3 main_function.py
        --data_path  数据路径
        --alpha1 垂直校正点垂直约束值
        --alpha2 垂直校正点水平约束值
        --beta1 水平校正点垂直约束值
        --beta2 水平校正点水平约束值
        --thet 目的地约束值
        --delta 每一米的增加的误差值
        --prob 是否使用第三题约束
        --top5 是否获取五条最优航迹
```
#### 第一题运行命令
```数据集1 sh ./run_data1.sh```

```数据集2 sh ./run_data2.sh```

#### 第二题先生成5跳最优路径长度再确定误差，类似命令
```
生成路径
数据集1 sh ./run_data1_top5.sh
数据集2 sh ./run_data2_top5.sh
```

```确定路径 python3   get_angle_route.py```

```生成误差 python3   generate_angle_route_error```

#### 第三题在第一题基础上直接改设置error值为5，命令
```生成路径 ```

```数据集1 sh ./run_data1_prob.sh```

```数据集2 sh ./run_data2_prob.sh```
