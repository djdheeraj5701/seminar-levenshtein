'''
Demonstrating Levenshtein edit distance(dp method)
on given word and finding closest word found in dictionary of words
stored in an array
'''
import datetime
import sys
# sys.stdin = open('sample.txt', 'r')
# sys.stdout = open('output.txt', 'w')
words=[]

def words_append():
    sys.stdin = open('sample.txt', 'r')
    for t in range(int(input())):
        words.append(input())
    print("sm2")


class Levenshtein:
    def __init__(self):
        self.dp=[]
    def initialise_dp(self,n,m):
        temp=[]
        for i in range(n + 1):
            x = []
            for j in range(m + 1):
                x.append(None)
            temp.append(x)
        self.dp=temp
    def levenshtein_dp(self,a, b, i, j):
        if b == "":
            self.dp[i][0] = len(a)
            return len(a)
        if a == "":
            self.dp[0][j] = len(b)
            return len(b)
        if self.dp[i][j] != None:
            return self.dp[i][j]
        c1 = self.levenshtein_dp(a[:i - 1], b[:j - 1], i - 1, j - 1) + (a[i - 1] != b[j - 1])  # replace
        c2 = self.levenshtein_dp(a[:i - 1], b, i - 1, j) + 1  # remove
        c3 = self.levenshtein_dp(a, b[:j - 1], i, j - 1) + 1  # insert
        self.dp[i][j] = min(c1, c2, c3)
        return self.dp[i][j]
    def solve_dp(self,b):
        start_time = datetime.datetime.now()
        nearest=[]
        minimum=float('inf')
        for a in words:
            self.initialise_dp(len(a),len(b))
            x=self.levenshtein_dp(a,b,len(a),len(b))
            if x<minimum:
                nearest=[a]
                minimum=x
            elif x==minimum:
                nearest.append(a)
        end_time = datetime.datetime.now()
        print(*nearest)
        print(end_time - start_time)
        gap = end_time - start_time
        return nearest, gap.seconds + gap.microseconds / 1000000


l=Levenshtein()
# l.solve_dp("clock")