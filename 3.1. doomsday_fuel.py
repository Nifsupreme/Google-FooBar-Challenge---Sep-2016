'''Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function answer(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) m = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
Output:
    (int list) [7, 6, 8, 21]

Inputs:
    (int) m = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
Output:
    (int list) [0, 3, 2, 9, 14]
'''


# SOLUTION

# Absorbing Markov Chain
# http://math.stackexchange.com/questions/193351/markov-chain-reach-one-state-before-another
# https://math.dartmouth.edu/archive/m20x06/public_html/Lecture14.pdf
# Solution:
# B = (I-Q)^-1 * R
# where Q is top-left matrix
# R is top right matrix

from fractions import Fraction

def copyMatrix(m):
    return copy.deepcopy(m)

def makeIdentity(n):
    result = make2dList(n,n)
    for i in xrange(n):
        result[i][i] = Fraction(1, 1)
    return result

def makeZero(n):
    result = make2dList(n,n)
    for i in xrange(n):
        result[i][i] = Fraction(0, 1)
    return result

def multiplyMatrices(a, b):
    # confirm dimensions
    aRows = len(a)
    aCols = len(a[0])
    bRows = len(b)
    bCols = len(b[0])
    rows = aRows
    cols = bCols
    # create the result matrix c = a*b
    c = make2dList(rows, cols)
    # now find each value in turn in the result matrix
    for row in xrange(rows):
        for col in xrange(cols):
            dotProduct = Fraction(0, 1)
            for i in xrange(aCols):
                dotProduct += a[row][i]*b[i][col]
            c[row][col] = dotProduct
    return c

def make2dList(rows, cols):
    a=[]
    for row in xrange(rows): a += [[0]*cols]
    return a


def multiplyRowOfSquareMatrix(m, row, k):
    n = len(m)
    rowOperator = makeIdentity(n)
    rowOperator[row][row] = k
    return multiplyMatrices(rowOperator, m)



def addMultipleOfRowOfSquareMatrix(m, sourceRow, k, targetRow):
    # add k * sourceRow to targetRow of matrix m
    n = len(m)
    rowOperator = makeIdentity(n)
    rowOperator[targetRow][sourceRow] = k
    return multiplyMatrices(rowOperator, m)



def invertMatrix(m):
    n = len(m)
    #assert(len(m) == len(m[0]))
    inverse = makeIdentity(n) # this will BECOME the inverse eventually
    for col in xrange(n):
        # 1. make the diagonal contain a 1
        diagonalRow = col
        #assert(m[diagonalRow][col] != 0) # @TODO: actually, we could swap rows
                                         # here, or if no other row has a 0 in
                                         # this column, then we have a singular
                                         # (non-invertible) matrix.  Let's not
                                         # worry about that for now.  :-)
        k = Fraction(1,m[diagonalRow][col])
        m = multiplyRowOfSquareMatrix(m, diagonalRow, k)
        inverse = multiplyRowOfSquareMatrix(inverse, diagonalRow, k)
        # 2. use the 1 on the diagonal to make everything else
        #    in this column a 0
        sourceRow = diagonalRow
        for targetRow in xrange(n):
            if (sourceRow != targetRow):
                k = -m[targetRow][col]
                m = addMultipleOfRowOfSquareMatrix(m, sourceRow, k, targetRow)
                inverse = addMultipleOfRowOfSquareMatrix(inverse, sourceRow,
                                                         k, targetRow)
    # that's it!
    return inverse



def lcm(a, b):
    return a * b // gcd(a, b)

def lcmm(*args):
    return reduce(lcm, args)
    
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
                
                
def subtractMatrices(A,B):
    C = makeZero(len(A))
    
    for i in xrange(0,len(A)):
        for j in xrange(0,len(A[i])):
            C[i][j] = A[i][j]-B[i][j]
    return C    

def printMatrix(a):
    def valueStr(value):
        if (isinstance(value, Fraction)):
            (num, den) = (value.numerator, value.denominator)
            if ((num == 0) or (den == 1)): return str(num)
            else: return str(num) + "/" + str(den)
        else:
            return str(value)
    def maxItemLength(a):
        maxLen = 0
        rows = len(a)
        cols = len(a[0])
        for row in xrange(rows):
            for col in xrange(cols):
                maxLen = max(maxLen, len(valueStr(a[row][col])))
        return maxLen
    if (a == []):
        # So we don't crash accessing a[0]
        print []
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print "[",
    for row in xrange(rows):
        if (row > 0) and (len(a[row-1]) > 1): print "\n  ",
        print "[",
        for col in xrange(cols):
            if (col > 0): print ",",
            # The next 2 lines print a[row][col] with the given fieldWidth
            format = "%" + str(fieldWidth) + "s"
            print format % valueStr(a[row][col]),
        print "]",
    print "]"

def answer0(m):


    for i in xrange(0,len(m)):
        for j in xrange(0,len(m)):
            if i==j:
                m[i][j]=1
    terminal = []
    nonterminal = []
    sums = []
     
    for i in xrange(0,len(m)):
        s = 0
        thesum = 0
        for j in xrange(0,len(m[i])):
            thesum += m[i][j]
            if m[i][j]!=0:
                s = m[i][j]
        if s==0 or (m[i][i]/thesum)>=1:
            terminal.append(i)
        #elif o:
        #    print("sup bitch")
        else:
            nonterminal.append(i)
        sums.append(thesum)
    
    for i in xrange(0,len(m)):
        for j in xrange(0,len(m)):
            m[i][j] = Fraction(m[i][j],sums[i])
            
    arr = nonterminal + terminal

    M = makeZero(len(m))
    printMatrix(m)
    # need to rearrange transition matrix to canonical form
    # this might help
    #http://www.aw-bc.com/greenwell/markov.pdf
    #https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/Chapter11.pdf
    for i in xrange(0,len(M)):
        for j in xrange(0,len(M)):
            i2 = arr[i]
            j2 = arr[j]
            M[i][j]=m[i2][j2]        
    
    
    Q = []
    R = []
    
    for i in xrange(0,len(nonterminal)):
        Q.append(M[i][0:len(nonterminal)])
        R.append(M[i][len(nonterminal):])
    
    if R == []:
        for i in xrange(0,len(terminal)):
            #Q.append(M[i][0:len(nonterminal)])
            R.append(M[i][len(nonterminal):])

    I = makeIdentity(len(nonterminal))
    ImQ = subtractMatrices(I,Q)

    N = invertMatrix(ImQ)
    if N==[]:
        B =R
    else:
        B = multiplyMatrices(N,R)
    
    
    lcs = []
    for i in xrange(0,len(B[0])):
        lcs.append(B[0][i].denominator)
    
    lc = lcmm(*lcs)
    
    F = make2dList(len(B),len(B[0])+1)
    for i in xrange(0,len(B)):
        for j in xrange(0,len(B[0])):
            F[i][j] = B[i][j]
    
    F[0][len(F[0])-1] = lc

    for j in xrange(0,len(F[0])-1):
        if F[0][j]>1:
            F[0][j] = 1
        else:
            F[0][j] = (F[0][j].numerator * lc / F[0][j].denominator)
        
    print(F[0])
    g = bool(1)
    if len(m)>1:
        #b = make2dList(len(m),len(m))
        #b[0][0] = bool(m[0][0] == 0)

        for j in xrange(0,len(F[0])):
            if F[0][j]<0:
                assert(0)
            #g = g  and F[0][j]<0
        
    
    return F[0]


mat = [[Fraction(1,1),Fraction(1,1),Fraction(0,1),Fraction(1,1)],\
       [Fraction(1,1),Fraction(1,1),Fraction(0,1),Fraction(1,1)],\
       [Fraction(0,1),Fraction(0,1),Fraction(0,1),Fraction(0,1)],\
       [Fraction(1,1),Fraction(1,1),Fraction(1,1),Fraction(1,1)]]

answer0(mat)

