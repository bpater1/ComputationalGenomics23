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
            elif P[j - 1] == '.' or T[i - 1] == P[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

if len(sys.argv) != 3:
    print("Usage: python hw4q1.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    with open(input_file, 'r') as file:
        T = file.readline().strip()
        P = file.readline().strip()

    # Initialize the minimum distance to be a large value
    min_distance = float('inf')

    # Check if P is a prefix of T
    if T.startswith(P):
        min_distance = min(min_distance, len(T) - len(P))
    
    # Iterate through all substrings of T
    for i in range(len(T)):
        distance = min_edit_distance(T[i:], P)
        min_distance = min(min_distance, distance)

    with open(output_file, 'w') as output:
        output.write(str(min_distance) + '\n')

except FileNotFoundError:
    print(f"File '{input_file}' not found.")
    sys.exit(1)