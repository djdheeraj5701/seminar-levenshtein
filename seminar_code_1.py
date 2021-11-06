'''
Levenshtein edit distance by dynamic programming
on two words "a" and "b" to show how close the words are
and how "a" can be transformed to "b"
'''
# a,b="potato","toooomaato"
# a,b="siens","science"
# a,b="rooflet","google"
a,b="teknologi","technology"
n,m=len(a),len(b)
dp=[]
for i in range(n+1):
    x=[]
    for j in range(m+1):
        x.append(None)
    dp.append(x)
dp[0][0]=0
def levenshtein_dp(a,b,i,j):
    if b=="":
        dp[i][0]=len(a)
        return len(a)
    if a=="":
        dp[0][j]=len(b)
        return len(b)
    if dp[i][j]!=None:
        return dp[i][j]
    c1=levenshtein_dp(a[:i-1],b[:j-1],i-1,j-1)+(a[i-1]!=b[j-1]) # replace
    c2=levenshtein_dp(a[:i-1],b,i-1,j)+1 # remove
    c3=levenshtein_dp(a,b[:j-1],i,j-1)+1 # insert
    dp[i][j]=min(c1,c2,c3)
    return dp[i][j]


# print("\nminimum edit required:",levenshtein_dp(a,b,n,m))
# print("\n?  ",end=" ")
# for i in b:
#     print(i,end=" ")
# print()
# print(" ",*dp[0])
# for i in range(1,n+1):
#     print(a[i-1],*dp[i])

dps=[]


def backtrack(a,b,i,j):
    if b=="":
        for k in range(i-1,-1,-1):
            dps.append(f"remove '{a[k]}'")
        return
    if a=="":
        for k in range(j - 1, -1, -1):
            dps.append(f"insert '{b[k]}'")
        return
    c1=levenshtein_dp(a[:i-1],b[:j-1],i-1,j-1)+(a[i-1]!=b[j-1]) # replace
    c2=levenshtein_dp(a[:i-1],b,i-1,j)+1 # remove
    # c3=levenshtein_dp(a,b[:j-1],i,j-1)+1 # insert
    if c1==dp[i][j]:
        if a[i-1]!=b[j-1]:
            dps.append(f"replace '{a[i-1]}' with '{b[j-1]}'")
        else:
            dps.append(f"'{a[i - 1]}'")
        backtrack(a[:i-1],b[:j-1],i-1,j-1)
    elif c2==dp[i][j]:
        dps.append(f"remove '{a[i-1]}'")
        backtrack(a[:i - 1], b, i - 1, j)
    else:
        dps.append(f"insert '{b[j-1]}'")
        backtrack(a, b[:j - 1], i, j - 1)
    return


# backtrack(a,b,n,m)
# while dps:
#     print(dps.pop())

