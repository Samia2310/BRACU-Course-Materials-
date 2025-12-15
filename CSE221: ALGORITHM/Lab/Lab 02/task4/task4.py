input = open("input4.txt","r")
output = open("output4.txt","w")

numbers = list(map(int,input.readline().split()))
number_of_inputs = numbers[0]
people = numbers[1]
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

end_sort = sorted(d2)
start_sort = [None]*len(end_sort)
idx = 0
for i in range(len(end_sort)):   #Sorted the end time then sort the index of starting time according to end time for the need of proceeding the code.
    idx = d2.index(end_sort[i])
    start_sort[i] = d1[idx]
check = [0]*people
check[0] = end_sort[0]
count = 1
idx = 1
for item in range(1,len(start_sort)):
   if idx < len(check):
       for k in range(len(check)):
            if check[k] == start_sort[item]:
              check[k] = end_sort[item]    #Creating a list with the length of the number of people.
              count += 1
              break               #allocate the first start-end time of the people and counted. Also when the end time matches with the next start time, count those also.
            elif end_sort[item-1] > start_sort[item]:
              check[idx] = end_sort[item]
              count += 1
              idx += 1
              break
for item in range(count,len(start_sort)):
  for j in range(1,people):
    if check[j-1] == start_sort[item]:
          check[j-1] = end_sort[item]   #If the end time matches with the next start time, count those.
          count += 1
          break
    elif check[j] == start_sort[item]:
          check[j] = end_sort[item]
          count += 1
    elif end_sort[item-1] < start_sort[item]:
        if (start_sort[item] - check[j-1]) > (start_sort[item] - check[j]):  #If the end time is immidiately less than the next start time, then satisfies the if condition.
          check[j] = end_sort[item]
          count += 1
        elif (start_sort[item] - check[j-1]) < (start_sort[item] - check[j]):
          check[j-1] = end_sort[item]
          count += 1
    elif end_sort[item-1] == start_sort[item]:
        if (start_sort[item] - check[j-1]) > (start_sort[item] - check[j]):
          check[j] = end_sort[item]
          count += 1
        elif (start_sort[item] - check[j-1]) == (start_sort[item] - check[j]):
          check[j-1] = end_sort[item]
          count += 1
    elif end_sort[item-1] > start_sort[item]:
        if (start_sort[item] - check[j-1]) > (start_sort[item] - check[j]):
          for k in range(len(check)):
            for m in range(k+1,len(check)):
                if start_sort[item] > check[k]:
                  if (start_sort[item] - check[k]) > (start_sort[item] - check[m]):
                    check[k] = end_sort[item]
                    count += 1
                    break
        elif (start_sort[item] - check[j-1]) < (start_sort[item] - check[j]):
          if len(check) == 2:
                if (start_sort[item] - check[0]) < (start_sort[item] - check[1]) and check[0]< start_sort[item]:
                    check[0] = end_sort[item]
                    count += 1
                elif (start_sort[item] - check[0]) < (start_sort[item] - check[1]) and check[1]< start_sort[item]:
                    check[1] = end_sort[item]
                    count += 1
                    break

output.write(f"{count}")