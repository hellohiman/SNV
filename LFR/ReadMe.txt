To run the program, under MS-DOS, type:



benchmark [FLAG] [P]


[FLAG] [P]



-N		number of nodes
 节点数
-k		average degree 平均度数
-maxk		maximum degree 最大度数
-mu		mixing parameter 混合参数
-t1		minus exponent for the degree sequence 

-t2		minus exponent for the community size distribution

-minc		minimum for the community sizes 社区最小规模节点数
-maxc		maximum for the community sizes 社区最大规模节点数
-on		number of overlapping nodes 重叠社区节点数
-om		number of memberships of the overlapping nodes

-C              average clustering coefficient 平均聚类系数

Example1:

lfr500	benchmark -N 500 -k 6 -maxk 25 -mu 0.1 -minc 15 -maxc 80

Example2:

 benchmark -f flags.dat -t1 3


If you want to produce a kind of Girvan-Newman benchmark, you can type:

 benchmark -N 128 -k 16 -maxk 16 -mu 0.1 -minc 32 -maxc 32

Output:
1) network.dat contains the list of edges (nodes are labelled from 1 to the number of nodes; the edges are ordered and repeated twice, i.e. source-target and target-source).


2) community.dat contains a list of the nodes and their membership (memberships are labelled by integer numbers >=1).


3) statistics.dat contains the degree distribution (in logarithmic bins), the community size distribution, and the distribution of the mixing parameter