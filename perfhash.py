
# File:    perfhash.py
# Author:  John Longley
# Date:    October 2026

# Template file for Inf2-IADS (2026-27) Coursework 1, Part A:
# Implementation of perfect hashing, adapting method of
# Belazzougui, Botelho and Dietzfelbinger, 2008.


# Provided code for simple mod hashing and bucket arrays.

def toInt(w):
    """Encodes a lowercase English word as an integer"""
    b = w.encode()
    t = 0
    for i in range(len(b)):
        t = t*27 + b[i] - 96
    return t

def modHash(s,p):
    """Simple mod hash with some coefficients for scrambling.
    Will take p prime for our outer hash"""
    return (toInt(s)*21436587 + 12345678912345) % p

# For the mini-hashes, the following simple enumeration works fine.
# Moduli needn't be prime, but we at least avoid multiples of 2 or 3.

def miniHash(m,j):
    """j-indexed family of hash functions with range 0,..,m-1"""
    d = j*6 + 3000001
    return (lambda w: modHash(w,d) % m)


# TODO: Task 1. Building a classic bucket-array hash table.

def buildHashTable(L,r,h):
    """Arrange items of L into r buckets using hash fun h with range 0,..,r-1.
    Returns the list of buckets."""
    buckets = [[] for _ in range(r)]
    for key in L:
        c = h(key)
        buckets[c].append(key)

    return buckets


def buildModHashTable(L,p):
    """Apply buildHashTable to the modHash function for p."""
    h = lambda w: modHash(w,p)
    return buildHashTable(L, p, h)

# TODO: Task 2. Computing mini-hash indices for a given list L of buckets,
#       using 0,...,m-1 as hash codes

def computeMiniHashIndices(L,m):
    """Compute suitable mini-hash indices for a given list L of buckets,
    where mini-hash funs have range 0,..,m-1"""

    L = enumerate(L)
    L = sorted(L, key= lambda p: len(p[1]), reverse = True)

    T = [False]*m
    R = [0]*len(L)

    for i, bucket in L:
        j = 0
        while True:
            h = miniHash(m,j)
            slots = set()

            for w in bucket:
                slot = h(w)
                if (T[slot] or slot in slots):
                    break
                slots.add(slot)
            else:
                break
            j += 1
        R[i] = j
        for slot in slots:
            T[slot] = True

    return R

# Provided code for putting all this together.

def isPrime(n):
    """Tests if n is prime"""
    if n%2 == 0 and n != 2:
        return False
    else:
        j = 3
        while j*j <= n:
            if n%j == 0: return False
            else: j += 2
        else: return True

def prevPrime(n):
    """Returns largest prime <= n, assuming n >= 3.
    Used to select a suitable modulus for the initial hash."""
    if n%2 == 0:
        return prevPrime(n-1)
    elif isPrime(n):
        return n
    else:
        return prevPrime(n-2)

class Hasher:
    """Compact data structure for representing a perfect hash function"""

    def __init__ (self,cMHI,keys,oload,load):
        """Builds perfect hasher from the following parameters.
           cMHI :  completed implementation of computeMiniHashIndices
           keys :  list of keys to be hashed
           oload : load on outer table, i.e. average bucket size
                   (higher oload means more compression but
                   hash function will be harder to construct)
           load :  desired load on resulting hash table, must be <= 1"""
        self.n = len(keys)
        self.r = prevPrime(int(self.n//oload))
        self.m = int(self.n//load)
        HT = buildModHashTable(keys,self.r)
        self.hashChoices = cMHI(HT,self.m)
        # results in a small data structure with no trace of keys!

    def hash (self,key):
        i = modHash(key,self.r)
        h = miniHash(self.m,self.hashChoices[i])
        return h(key)


class HashDict:
    """Implementation of dictionaries via perfect hashing"""

    def buildFlatTable(keyvals,H):
        """Helper function for constructor.
        Assuming H is perfect for the keys appearing in keyvals,
        builds table of in-place key-value pairs (no buckets)."""
        HT = buildHashTable(keyvals, H.m, lambda kv: H.hash(kv[0]))
        # HT will have <= 1 item per bucket, so can flatten the list:
        return [None if b==[] else b[0] for b in HT]

    # Constructor:
    def __init__(self,cMHI,keyvals,oload,load):
        """Builds dictionary.
           cMHI is completed implementation of computeMiniHashIndices
           keyvals should be a list of lists [k,v], to allow v to be updated.
           oload and load are as in Hasher class."""
        self.cMHI = cMHI
        self.oload = oload
        self.load = load
        keys = [kv[0] for kv in keyvals]
        self.H = Hasher(cMHI,keys,oload,load)
        self.T = HashDict.buildFlatTable(keyvals,self.H)


# TODO: Task 3: lookup and setValue methods.

    def lookup(self,k):
        """Return value associated with k, or None if k not present"""
        entry = self.T[self.H.hash(k)]
        if entry is not None and entry[0] == k:
            return entry[1]
        return None

    def setValue(self,k,v):
        """If k is present, update value to v. Return whether k present."""
        entry = self.T[self.H.hash(k)]
        if entry is not None and entry[0] == k:
            entry[1] = v
            return True
        return False


# TODO: Task 4: Towards an insert method

    def insert(self,k,v):
        """Insert pair k,v into dictionary, where k is new."""
        H, T, slot = self.H, self.T, self.H.hash(k)
        if T[slot] is None:
            T[slot] = [k,v]
        elif T[slot][0] != k:
            i = modHash(k,H.r)
            bucket = [kv for kv in T if kv and modHash(kv[0],H.r) == i]

            for kv in bucket: T[H.hash(kv[0])] = None
            bucket.append([k,v])
            for j in range(H.m//4):
                slots = {miniHash(H.m,j)(kv[0]) for kv in bucket}
                if len(slots)==len(bucket) and not any(T[s] for s in slots):
                    H.hashChoices[i] = j
                    for kv in bucket: T[H.hash(kv[0])] = kv
                    return

            pairs = [kv for kv in T if kv is not None] + bucket
            self.__init__(self.cMHI, pairs, self.oload, self.load)

# [Discussion goes here]
# [Add further comment lines as necessary]
#

    
# For testing: Loading in a word list

def removeNewline(s):
    if (s[-1] == '\n'):
        return s[:-1]
    else:
        return s

def wordlist(filename):
    reader = open(filename,'r')
    words = [removeNewline(line) for line in reader]
    reader.close()
    return words

# Example:

# keys = wordlist('enable.txt')


## End of file
