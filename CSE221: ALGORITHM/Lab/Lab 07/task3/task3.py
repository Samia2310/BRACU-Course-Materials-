input = open("input3.txt", "r")
output = open('output3.txt', 'w')

num = int(input.readline().strip())
    
def climb_stairs(num):
    if num == 0:
        return 1
    if num == 1:
        return 1
    
    dp = [0] * (num + 1)
    dp[0] = 1 
    dp[1] = 1 
    
    for i in range(2, num + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[num]

result = climb_stairs(num)
output.write(f'{result}')

input.close()
output.close()
