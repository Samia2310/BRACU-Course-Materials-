input = open("input1a.txt","r")
output = open("output1a.txt","w")

first_line = list(map(int,input.readline().split(" ")))
number_of_inputs = first_line[0]
L1 = [first_line[1]]
L2 = list(map(int,input.readline().split(" ")))
flag = True
for i in range(len(L2)):       #testing every single element of L1 with every single element of L2.
  for j in range(i+1,len(L2)):
    if L2[i] + L2[j] == L1[0]:
      flag = False
      output.write(f"{i+1} {j+1}")       #After getting the desired output, break the loop. Otherwise, print "Impossible".
      break
  if flag == False:
      break
if flag == True:
  output.write("Impossible")