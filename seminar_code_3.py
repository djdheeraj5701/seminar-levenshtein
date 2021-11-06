'''
Demonstrating Levenshtein edit distance(modified dp method)
on given word and finding closest word found in dictionary of words
stored in a Trie
'''
import sys,datetime
sys.stdin = open('sample.txt', 'r')
# sys.stdout = open('output.txt', 'w')
sys.setrecursionlimit(10**6)

class Node:
    def __init__(self,ch):
        self.char=ch
        self.next=[None for i in range(26)]
        self.wordend=False
    def endwordhere(self):
        self.wordend=True
    def iswordend(self):
        return self.wordend
    def addnext(self,node):
        self.next[ord(node.char)-ord('a')]=node

class Trie:
    def __init__(self):
        self.root=Node("")
    def addword(self,word):
        temp=self.root
        i=0
        try:
            while i<len(word) and temp.next[ord(word[i])-ord('a')]:
                temp=temp.next[ord(word[i])-ord('a')]
                i+=1
        except:
            print(i,word)
        if i==len(word):
            if temp.iswordend():
                # print(f"{word} already exists")
                pass
            else:
                temp.endwordhere()
                # print(f"{word} added")
            return
        wl=list(Node(i) for i in word[i:])
        for j in range(1,len(word)-i):
            wl[j-1].addnext(wl[j])
        wl[-1].endwordhere()
        temp.addnext(wl[0])
        # print(f"{word} added")
    def searchword(self,word):
        temp = self.root
        i = 0
        while i<len(word) and temp.next[ord(word[i]) - ord('a')]:
            temp = temp.next[ord(word[i]) - ord('a')]
            i += 1
        if i == len(word) and temp.iswordend():
            return True
        return False
    def dfs(self,curr,word=""):
        if curr.wordend:
            yield word
        for i in range(26):
            if curr.next[i]!=None:
                yield from self.dfs(curr.next[i],word+curr.next[i].char)

dictionary = Trie()
def words_append():
    sys.stdin = open('sample.txt', 'r')
    for t in range(int(input())):
        # print(t)
        x=input()
        for i in x:
            if not (ord('a')<=ord(i)<=ord('z')):
                break
        else:
            dictionary.addword(x)
    print("sm3")


class Levenshtein:
    def __init__(self):
        self.dp=[]
        self.count=float('inf')
    def initialise_dp(self,n,m):
        temp=[]
        for i in range(n + 1):
            x = []
            for j in range(m + 1):
                x.append(None)
            temp.append(x)
        self.dp=temp
    def levenshtein_dp(self,a, b, i, j):
        if abs(i-j)>self.count:
            return abs(i-j)
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
    def find_nearest(self,b):
        start_time=datetime.datetime.now()
        nearest = []
        yg=dictionary.dfs(dictionary.root)
        while True:
            try:
                a=yg.__next__()
                self.initialise_dp(len(a), len(b))
                x = self.levenshtein_dp(a, b, len(a), len(b))
                if x < self.count:
                    nearest = [a]
                    self.count = x
                elif x == self.count:
                    nearest.append(a)
            except:
                break
        end_time = datetime.datetime.now()
        print(*nearest)
        print(end_time-start_time)
        gap = end_time - start_time
        return nearest, gap.seconds + gap.microseconds / 1000000




l=Levenshtein()
# b='clockk'
def solver(b):
    if not dictionary.searchword(b):
        return l.find_nearest(b)
    else:
        return [b],0