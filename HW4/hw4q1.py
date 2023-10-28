import sys

def min_edit_distance(T, P):
    m, n = len(T), len(P)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif T[i - 1] == P[j - 1] or P[j - 1] == '.':
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

if len(sys.argv) != 3:
    print("Usage: python3 hw4q1.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    with open(input_file, 'r') as file:
        T = file.readline().strip()
        P = file.readline().strip()

    distance = min_edit_distance(T, P)

    with open(output_file, 'w') as out_file:
        out_file.write(str(distance) + '\n')

except FileNotFoundError:
    print(f"File '{input_file}' not found.")
    sys.exit(1)