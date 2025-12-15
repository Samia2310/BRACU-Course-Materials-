input = open('input1.txt', 'r')
output = open('output1.txt','w')

data = input.readlines()

first_line = data[0].strip()
N, K = map(int, first_line.split())

parent = list(range(N+1))
size = [1] * (N+1)

result = []

def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, size, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)
    
    if rootX != rootY:
        if size[rootX] < size[rootY]:
            parent[rootX] = rootY
            size[rootY] += size[rootX]
            return size[rootY]
        else:
            parent[rootY] = rootX
            size[rootX] += size[rootY]
            return size[rootX]
    return size[rootX]

for i in range(1, K+1):
    A, B = map(int, data[i].strip().split())
    cir_size = union(parent, size, A, B)
    result.append(cir_size)


for item in result:
    output.write(f'{item}\n')

input.close()
output.close()