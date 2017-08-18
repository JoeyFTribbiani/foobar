def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def simplify(nums):
    gcdV = 0
    for e in nums:
        gcdV = gcd(gcdV, e)
    return [e / gcdV for e in nums]


# suppose m[s1][s2] is the amount of sum of the m[s2],
# then I can add m[s2] to m[s1]
def mergeToS1(m, s1, s2):
    rest = set(range(len(m))) - {s1, s2}
    res = [0] * len(m)
    sumS2 = sum(m[s2])

    # m[s2][e] + m[s1][e]*sumS2/m[s1][s2]
    for e in rest:
        res[e] = sumS2 * m[s1][e] + m[s1][s2] * m[s2][e]
    m[s1] = simplify(res)


'''
This problem was quite tricky.
I took a long time to figure this out.
Here, I just need to count proportion for the terminal state.
So the basic idea is to merge all the intermediate states.
'''


def answer(m):
    # self transition
    for i in range(len(m)):
        m[i][i] = 0
    sums = [sum(s) for s in m]
    terms = [i for i in range(len(sums)) if sums[i] == 0]
    notTerms = list(set(range(len(m))) - set(terms))

    for j in range(len(notTerms) - 1, -1, -1):
        for i in range(j):
            mergeToS1(m, notTerms[i], notTerms[j])

    res = [m[0][e] for e in terms]
    if sum(res) == 0:
        res = [1] * len(res)
    res += sum(res),
    return simplify(res)
