input = open("input3.txt","r")
output = open("output3.txt","w")

number_of_inputs = int(input.readline())
#appending each time slot in the time list
time = []
for item in range(num):
    line = list(map(int,input.readline().split()))
    time.append(line)

d1 = []
d2 = []
for elem in time:
    d1.append(elem[0])
    d2.append(elem[1])
start_L = []
end_L = []
for i in range(len(d1)):
  if d1[i] > 0:                    #making two new lists of the start time & end time excluding 0.
    start_L.append(d1[i])
    end_L.append(d2[i])
end_sort = sorted(end_L)               #Sorted the end time then sort the index of starting time according to end time for the need of proceeding the code.
start_sort = [None]*len(end_sort)
idx = 0
for i in range(len(end_sort)):
    idx = end_L.index(end_sort[i])
    start_sort[i] = start_L[idx]

L = []
Count = 0
for i in range(len(start_L)-1):
  task = end_sort[Count]             
  if start_sort[i] > task:              
    if end_sort[i] >= start_sort[i+1]: 
      L.append(start_sort[i])
      Count += 1              
  elif start_sort[i] == task:   
    Count += 1
    L.append(start_sort[i])
if start_sort[len(end_sort)-1] > end_sort[len(start_sort)-1-1]:   
    L.append(start_sort[len(start_sort)-1])
if start_sort[len(end_sort)-1] == end_sort[len(start_sort)-1-1]:  #Here, all the desired start time appnded in list "L".
    L.append(start_sort[len(start_sort)-1])
idx = 0
end = [end_sort[0]]
start = [start_sort[0]]
for i in range(len(end_sort)):
  if idx < len(L):
    if start_sort[i] == L[idx]:          #Finding cooresponding end time of starting time of L.
      start.append(start_sort[i])
      end.append(end_sort[i])
      idx += 1
output.write(f"{idx+1}\n")
for i in range(len(start)):
    output.write(f'{start[i]}  {end[i]}\n')  
