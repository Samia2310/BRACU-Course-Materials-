input_file = open("input2a.txt","r")
output_file = open("output2a.txt","w")

number_of_inputs1 = int(input_file.readline())
L1 = list(map(int,input_file.readline().split()))
number_of_inputs2 = int(input_file.readline())
L2 = list(map(int,input_file.readline().split()))
new_arr = [None]*(len(L1)+(len(L2)))  #created a new array with the length of total given two sorted list.
for i in range(len(L1)):
  new_arr[i] = L1[i]           #appending both sorted in new_arr.
  idx = i+1
for i in range(len(L2)):
  new_arr[idx] = L2[i]
  idx += 1
sort_arr = sorted(new_arr) #sorted new_arr
for i in sort_arr:
  output_file.write(f"{int(i)  }")    #Print the output.