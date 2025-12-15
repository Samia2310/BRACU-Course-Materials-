input = open('input4.txt', 'r')
output = open('output4.txt' , 'w')

data = input.readlines()

N, X = map(int, data[0].split())
coins = list(map(int, data[1].split()))

def minCoins(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  
    for item in coins:
        for i in range(item, amount + 1):
            dp[i] = min(dp[i], dp[i - item] + 1)
    
    if dp[amount] != float('inf'):
      return dp[amount]
    else:
      return -1

result = minCoins(coins, X)
output.write(f'{result}')

input.close()
output.close()