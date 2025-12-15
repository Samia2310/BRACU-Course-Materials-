input = open('input2.txt', 'r')
output = open('output2.txt','w')

data = input.readlines()

N, M = map(int, data[0].split())

edges = []
index = 1
for i in range(M):
    u, v, w = map(int, data[index].split())
    u -= 1 
    v -= 1  
    edges.append((w, u, v))
    index += 1

edges.sort()

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u]) 
        return self.parent[u]
    
    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
            return True
        return False

union_find = UnionFind(N)
mst_cost = 0
edges_in_mst = 0

for w, u, v in edges:
    if union_find.find(u) != union_find.find(v):  
        if union_find.union(u, v):  
            mst_cost += w
            edges_in_mst += 1
            if edges_in_mst == N - 1:
                break

output.write(f'{mst_cost}')

input.close()
output.close()