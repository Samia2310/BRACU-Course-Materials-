input = open("input1b.txt","r")
output = open("output1b.txt","w")

first_line = list(map(int,input.readline().split(" ")))
number_of_inputs = first_line[0]
L1 = [first_line[1]]
L2 = list(map(int,input.readline().split(" ")))
frst_pointer = 0
last_pointer = len(L2)-1           #Here, frst_pointer is the first index of the list initially and last_pointer is last index of the list initially.
flag = True
for i in range(len(L2)):
  if L2[frst_pointer]  + L2[last_pointer] == L1[0]:   
    flag = False
    output.write(f"{frst_pointer+1} {last_pointer+1}")
  elif frst_pointer  + last_pointer < L1[0]: #If the sum of the element of frst_pointer & last_pointer is less than the given number then we increase the frst_pointer.
    frst_pointer = frst_pointer + 1
  else:
    last_pointer = last_pointer - 1  ##If the sum of the element of frst_pointer & last_pointer is greater than the given number then we increase the last_pointer.
  if flag == False:
    break
if flag == True:       #If the sum of the element of frst_pointer & last_pointer is equal to the given number the print the positions of the two elements. Otherwise, print "Impossible".
  output.write("Impossible")