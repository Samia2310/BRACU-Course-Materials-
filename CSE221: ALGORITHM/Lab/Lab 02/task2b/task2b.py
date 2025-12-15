input_file = open("input2b.txt","r")
output_file = open("output2b.txt","w")

number_of_inputs1 = int(input_file.readline())
L1 = list(map(int,input_file.readline().split()))
number_of_inputs2 = int(input_file.readline())
L2 = list(map(int,input_file.readline().split()))
frst_pointer = 0
scnd_pointer = 0
new_arr = [None]*(len(L1)+len(L2))  #Here, frst_pointer is the first pointer of the first list and scnd_pointer is the first pointer of second list.
for i in range(len(L1)+len(L2)):
  if frst_pointer < len(L1) and scnd_pointer < len(L2): #This "if" condition will be satisfied till the frst_pointer is less than the length of first list and the scnd_pointer is less than the length of second list.
      if L1[frst_pointer] > L2[scnd_pointer]:  #If the element of the first list is greater than the element of second list, then the lesser element means the element of second list will be appended to new_arr & scnd_point will be increased with 1.
        new_arr[i] = L2[scnd_pointer]
        scnd_pointer += 1
      elif L1[frst_pointer] < L2[scnd_pointer]: #If the element of the second list is greater than the element of first list, then the lesser element means the element of first list will be appended to new_arr & frst_point will be increased by 1.
        new_arr[i] = L1[frst_pointer]
        frst_pointer += 1
      elif L1[frst_pointer] == L2[scnd_pointer]: #If the element of the first list is equal to the element of second list, then the element of first list will be appended to new_arr & frst_point will be increased by 1.
        new_arr[idx] = L1[frst_pointer]
        frst_pointer += 1
      idx = i+1
if frst_pointer == len(L1):                    #If the frst_pointer is equal to the len(L1), then the left elements of L2 is copying here as the list is sorted.
    copyleftelem = L2[scnd_pointer : len(L2):]
elif scnd_pointer == len(L2):          #If the scnd_pointer is equal to the len(L2), then the left elements of L1 is copying here as the list is sorted.
    copyleftelem = L1[frst_pointer:len(L1):]
ind = 0
for j in range(idx,len(new_arr)):
    new_arr[j] = copyleftelem[ind]   #Then the copied elements pasted in the new_arr.
    ind = ind+1
for i in new_arr:
  output_file.write(f"{int(i) }")  