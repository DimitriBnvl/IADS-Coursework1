# **Informatics 2 – Introduction to Algorithms and Data Structures (2026–27)** Coursework 1: Perfect Hashing and Space-Saving Red-Black Trees 

John Longley 

October 23, 2026 

This is a Python programming practical in two independent parts, bearing equal weight. In Part A, you will implement a scheme for _perfect hashing_ for a given set of keys, giving a flavour of state-of-the-art work in this area, and use it to create an efficient dictionary implementation. In Part B, you will implement `lookup` and `insert` operations for an implementation of dictionaries via _red-black trees_ — one that will be more space-efficient than most classic tree implementations. Part B (especially) will require a grasp of the organization of program memory as explained in Lecture 6. The purpose of the coursework is to develop and assess your understanding of the material from Lectures 6–10 and your ability to translate the ideas into Python code. 

This is a non-credit-bearing coursework assignment. You are permitted to approach it in any way that’s helpful for your learning—for instance, to collaborate with other students, or to make selective use of AI tools. However, we’d respectfully ask that you don’t submit code that is written _entirely_ by AI with no input from yourself: this would be of no benefit for your learning of the course material, and would merely waste the time of the human markers. 

The deadline is **12 noon on Friday 13 November** . The coursework will be marked out of 100, using a combination of automarker tests on Gradescope and inspection by a human marker. You will receive fairly detailed feedback on your Python code, both automated and human. Your marks and feedback will be returned to you by Friday 28 November. 

To get started, you’ll need the template files `perfhash.py` and `redblak.py` , and also (for testing of Part A) the text file `enable.txt` . All these are available from the Learn Assessment page. In each of the template files, some Python code is provided for you, and your task is to complete the implementation by adding function or method definitions at the points marked `# TODO` . In each case, please work with the function headers you are provided with — you must not change the number, order or names of the arguments. Some general points: 

1. It’s assumed that you are familiar with the basics of Python programming as covered by the three **lab sheets** available from the Semester 1 schedule page on OpenCourse. If you require help on the Python side of things, we will be offering **lab sessions** during Weeks 7 and 8 (i.e. 2–13 November), at times and venues to be advertised on the OpenCourse site and by email. You’re also welcome to post Python-related questions (or any other queries about the coursework) to the course’s **EdStem forum** — however, please check through previous postings first to see whether your question 

has already been asked and answered! We’ll try where possible to answer queries within 48 hours. You are also encouraged to help one another (and us) by responding to queries if you know the answer (but see point 8 below). 

2. The total volume of Python code you’re expected to write is not vast. My own implementation involves around 60 lines of code for Part A and 80 lines for Part B. Don’t worry if your version is a little longer or shorter than this — but if you find yourself writing twice as much, you should pause to ask yourself whether there’s a simpler approach. 

3. The autotests will be run by Gradescope using a current version of Python 3; in practice, any Python 3 version will suffice for developing your code. For this coursework, you’re _not_ permitted to import any Python libraries other than those already imported by the provided code. The point in this coursework is to implement everything from the ground up. 

4. Because the coursework will be largely automarked, it’s very important that you comply with the instructions precisely, e.g. as regards the names of functions, what arguments they take, and what they return. The required function headers are included in the template files. It’s also important that you make no changes to the provided code, and add new code _only_ at the points indicated. 

For each of the functions you implement, the automarker will run a number of tests to assess the correctness and (in some cases) time-efficiency of your code. Any code that doesn’t suffer from a clear algorithmic inefficiency should pass these tests, so no need to fine-tune your code for those last few percentage points in runtime. The human marker will then assess your code for space-efficiency and use of appropriate algorithms, and may adjust the automark either positively or negatively. 

5. You should give some attention to matters of code style, as there will be a few marks allocated for this. In particular: 

   -  Your code should be _formatted_ so that it is clear and easy to read. Some good advice on this is given in Python’s PEP 8 style guide: 

### `https://peps.python.org/pep-0008/` 

It’s good practice to get into the habit of following these recommendations, though we won’t mark you on whether you comply with them exactly. 

-  All lines should be strictly limited to a maximum of 79 characters. 

-  Variable names should be sensibly chosen, and informative where possible, but remember that longer names can make the code hard to read overall. Short names are preferred for variables that are only used locally within a small region of the code (which will be the case for most or all of the variables you introduce). 

-  You should add a modest number of **short comments** to your code where they help to make it more readable. However, this should be done quite sparingly, as over-commenting can be counterproductive. Put yourself in the shoes of a human marker with a tight time budget of 15 minutes per student submission: you’re wanting to steer their thoughts in the right direction as quickly as possible. Where possible, it’s best if the code is sufficiently clear that it speaks for itself. 


For some excellent guidance on these sorts of things, which will be equally important in _all_ courses that involve programming, we recommend Perdita Stevens’s book _How to write good programs_ (Cambridge University Press), which includes examples in Java, Python and Haskell. 

6. It’s your responsibility to **test** all of your code thoroughly before you submit it. You should expect to spend some time devising and constructing your own tests to ensure that your various functions work correctly in all cases — this is an important skill to develop. Before submitting, it’s worth checking that your code runs correctly on Python as installed on the DICE machines (the autograding will actually be done on Gradescope’s machines using a similar setup). As a bare minimum, please ensure that your files load correctly into Python without any syntax errors — if they don’t, we won’t even be able to run the autotests and _very few_ marks will be available.<sup>1</sup> 

7. Please don’t be surprised or disheartened if it takes some time to get your code to work! This is _perfectly normal_ , even for seasoned programmers — so allow yourself a generous amount of time for debugging. Tracking down an elusive bug can be timeconsuming and deeply frustrating, but this too is an important practical skill that can be acquired only by experience. 

8. Although collaboration is permitted, it is forbidden to share any part of a solution attempt in a public posting on EdStem or any other forum. Those students who wish to work entirely by themselves should be free to do so without unintentionally seeing other students’ work in passing. If copying and pasting a Python error message, please check that it doesn’t have a fragment of your code embedded within it. 

## **Part A: A modern perfect hashing algorithm [50 marks]** 

As explained in Lecture 8, a _perfect hash_ function for a fixed set _S_ of keys is a function # : _S →{_ 0 _, . . . , m −_ 1 _}_ (for some chosen _m_ ) such that no two keys map to the same integer. A perfect hash function # is _minimal_ if _m_ = _|S|_ , so that # is actually a bijection _S →{_ 0 _, . . . , m −_ 1 _}_ . If we are able to find a perfect hash function for a given set of keys, we can implement a hash table for these keys with fast worst-case lookup. Such schemes (including minimal ones) have found practical applications in databases, computer networks, compressed text indexing, language models, and other areas. 

The method we follow is due to Belazzougui, Botelho and Dietzfelbinger (2009), and enables us to construct perfect hash functions that can be represented very compactly in memory. A similar approach (with added bells and whistles) is also employed by more recent state-of-the-art work in the area.<sup>2</sup> The instructions below give all the information you will need, but the file `BBD-slides.pdf` , available from Learn, may serve as a useful supplement (including some pictures). 

Take a look at the template file `perfhash.py` . There is some simple machinery for hashing of strings over `a..z` modulo a number `p` . The precise details aren’t important, but you should experiment a bit with the function `modHash` to see what it does. There is then a function `miniHash` which, for a given number `m` , yields a whole family of (reasonably ‘independent’) hash functions mapping strings to integers `0,...,m-1` . For example: 

> 1A common source of problems in Python coursework is incorrect indentation. E.g. a method that’s supposed to be part of a class definition may fail to be treated as such if the indentation indicates that the class definition has already finished. This may be something to double-check in case of problems. 

> 2See for example G.E. Pibiri and R. Trani, _PTHash: Revisiting FCH Minimal Perfect Hashing_ , SIGIR 2021.

### `miniHash(1000,0)(’aardvarks’) miniHash(1000,1)(’aardvarks’)` 

Our goal is to construct a _perfect hash function_ mapping a specified list of `n` English words (given by `keys` ) to integers `0,...,m-1` for some specified `m` . (The intention is that `m >= n` , but that `m` is not _much_ larger than `n` .) The method proceeds as follows. 

First, we ‘mod hash’ our set of keys down to numbers `0,...,r-1` , where `r` is some suitable prime number (chosen by code later in the file). This results in a list `L` of `r` _buckets_ , where each bucket is itself a (possibly empty) list of strings. This is the purpose of Task 1 below. 

Next, we try to find for each of these buckets a number `j` such that `miniHash(m,j)` is a suitable mini-hash function to apply to the strings in that bucket. ‘Suitable’ means that all of these mini-hash functions _taken together_ should map the contents of all buckets to codes `0,...,m-1` with no clashes. 

Your main challenge (Task 2 below) will be to write a function `computeMiniHashIndices(L,m)` that takes a list `L` of buckets (that is, a list of lists of strings over `a..z` ) and a desired table size `m` , and suitably selects a number `j` for each bucket as above, storing the number `j` for the `i` th bucket at position `i` in a list `R` , whose length is the number `r` of buckets (i.e. the length of `L` ). This list `R` is what your function should return; it will become the value of the field `hashChoices` in the `Hasher` class. The `hash` method for this class then gives the hash function we have constructed, which is intended to be a perfect hash function. 

How do we go about choosing `j` -values to ensure this? We proceed as follows: 

-  First, sort the list of buckets `L` in order of decreasing size. Within the sorted list, we will want each bucket to be paired with a number `i` indicating the position in the original list `L` where this bucket came from: thus, each entry in the sorted list will be a pair `(i,L[i])` for some `i` . 

-  Create a list `T` of `m` booleans, initially all `False` , intended to record which slots in the main table are currently ‘taken’. Also create a list `R` of integers (initially zero), one for each bucket. 

-  Go through the buckets in order of decreasing size. For each bucket `B` , search for the smallest integer `j >= 0` such that the mini-hash function `miniHash(m,j)` is _suitable_ for `B` . This means that: 

   - it maps all elements of `B` to currently free slots in the main table, 

   - it doesn’t map any two elements of `B` to the same slot. 

Once a suitable value of `j` is found,<sup>3</sup> record this value as `R[i]` (where `i` is the original position of the bucket `B` ), and mark all the slots to which we are sending elements of `B` as ‘taken’. 

The provided class `Hasher` will use your code to create a perfect hash table. Task 3 will then use this to create a dictionary implementation with fast lookup. 

Although the spirit of this scheme is to working with a _fixed_ set of key-value pairs, it’s also interesting to ask what it would take to allow for occasional changes to this set. This is investigated in Task 4, where you are invited to implement a simple insert method for your dictionary, and discuss its limitations. 

> 3Actually, there’s no absolute guarantee that a suitable `j` will _ever_ be found. But as long as our mini-hash functions are ‘sufficiently random and independent’, this will happen ‘almost certainly’, and the approach works extremely well in practice. You need not worry about the possibility that the search will fail. 
 

- **Task 1 (6 marks).** The first task is to write some simple code for constructing classic bucket-array hash tables. At the point marked `# TODO: Task 1` , provide implementations for the following two functions. 

   -  (4 marks.) A function `buildHashTable` which, given a list of keys `L` , a desired table size `r` and a hash function `h` mapping the keys to integers `0,..,r-1` , returns the corresponding list of `r` buckets, with the bucket for each hash code `c` appearing at position index `c` . Each bucket should itself be a list of keys (possibly empty). 

   -  (2 marks.) A function `buildModHashTable` that calls the above to create a hash table of a given size `p` using the `modHash` function (as defined earlier in the file) with modulus `p` . (Hint: Use Python’s `lambda` construct.) Again, this should return a list of buckets as above. 

- **Task 2 (22 marks).** At `# TODO: Task 2` , implement `computeMiniHashIndices(L,m)` as described above, returning a list of mini-hash indices, one for each bucket, in the order in which the buckets appear in `L` . Although the task may seem complicated, the list comprehension syntax of Python allows it to be coded quite economically. (As a rough guide, my own implementation takes 26 lines including comments.) You may define any helper functions you find useful (although my implementation doesn’t have any). 

In this part, you _are_ permitted to use Python’s built-in `sort` method, and this may be helpful — consult the Python Standard Library documentation for details. 

You will now be able to construct perfect hash tables as follows. Set `keys` to be a list of English words, for example the one in the file `enable.txt` .<sup>4</sup> (Such a list can be loaded in using the `wordlist` function defined at the end of the template file). Then type e.g. 

```
H=Hasher(computeMiniHashIndices,keys,5.0,0.8)
```

This should succeed within a few seconds, using your code to build a data structure `H` which can then be used for fast hashing (e.g. `H.hash(’aardvarks’)` ). The parameter 5.0 approximately determines the average bucket size used (via `r` _≃_ `n/5.0` ): the higher this parameter, the more compact the resulting data structure `H` , but the longer it may take to find suitable indices.<sup>5</sup> The parameter 0.8 gives the load for the resulting hash function (so that `m = n/0.8` ); again, the closer this parameter is to 1.0, the less space we waste, but the harder our Hasher will be to construct. Taking 1.0 for this parameter gives us a _minimal_ perfect hashing — this should succeed within a few seconds with an average bucket size of around 3.0, but it may struggle with higher bucket sizes. Note too that the `Hasher` constructor requires you to pass your implementation of `computeMiniHashIndices` as a parameter—this is for reasons associated with the automarker. 

It’s not too hard to check that your `H` really is a perfect hasher by using the provided function `buildHashTable` to build an ordinary bucket-list hash table from it, then 

> 4See e.g. `https://www.bananagrammer.com/2013/12/the-amazing-enable-word-list-project.html` 

> 5For reasonable parameter choices, the space occupied by `H` will not exceed 3 or 4 bits per key (independently of the sizes of the keys)! This is obviously tiny compared with the keys themselves, let alone any values we might associate with them. 
 

checking that this contains no buckets of length _>_ 1. This will entail writing a small amount of test code and we recommend that you try this, but please do not submit this extra code. 

_Marking for Task 2_ : 16 marks for correctness and 6 marks for efficiency. The efficiency marks here are intentionally somewhat hard to get—any serious algorithmic efficiency may cost you these marks, though minor inefficiencies in the coding style will probably not matter. 

- **Task 3 (6 marks).** Later in the file, you will find a template for a class `HashDict` which uses minimal perfect hashing to provide a dictionary implementation with fast lookup. The constructor, which is already provided, creates such a dictionary from a given set of key-value pairs, subject to some parameters. Study this to understand how it works. Note that each key-value pair should be supplied as a list `[k,v]` rather than a tuple `(k,v)` — this is so that we can later update the `v` component if we wish. 

Your task here is to provide implementations of the following two methods, at the point marked `# TODO: Task 3` . 

-  (3 marks.) `lookup(self,w)` : Returns the value associated with the key `w` . Should return `None` if `w` is not present in the dictionary, or if `None` is associated with `w` . 

-  (3 marks.) `setValue(self,w,v)` : Updates the value associated with `w` (if present) to `v` . Should return `True` if `w` is present and the update succeeds, or `False` if `w` is not present. 

Both implementations should run in Θ(1) time, i.e. within a time bound independent of the number of keys. 

You should devise a way to test the resulting `HashDict` implementation on a suitable list of key-value pairs. Again, you need not submit your test code. 

- **Task 4 (12 marks).** For the last task, you are invited to consider what it would take to add an `insert` method for adding a new key-value pair to the dictionary (where the key is not one already present). This will inevitably involve some costly work in some cases, but you should think about how the problem might be mitigated. 

   -  (8 marks.) At the point marked `# TODO: Task 4` , provide a simple working implementation of a method `insert(self,k,v)` that inserts the new pair `[k,v]` into the dictionary if `k` is not already present. (If `k` is already present, `insert` should return immediately without doing anything.) Your implementation should be the best you can achieve within _at most 20 lines of code_ (including helper functions and comments, but excluding blank lines). Don’t worry if your implementation adopts a seemingly crude approach in some situations. 

   -  (4 marks.) Immediately below your `insert` implementation, add up to 12 lines of English text as comments (max 79 characters per line), informally discussing one or more possible ways in which, with further work, your implmentation might be improved on, and to what extent these would solve the problems. 

- **The final 4 marks** for Part A will be awarded by the human marker for code clarity and style (good structure, formatting, choice of names, commenting etc.) as described on page 2 of these instructions. 


## **Part B: Space-efficient red-black trees [50 marks]** 

Before attempting this part, make sure you are familiar with the material on red-black trees from Lecture 9. Your task will be to provide implementations of the `lookup` and `insert` methods in a red-black tree implementation of dictionaries. 

Take a look at the template file `redblack.py` . You will see a class `Node` for representing nodes of a tree: these carry key-value pairs as well as pointers to left and right children. (The special object `None` does duty for all trivial leaf nodes.) In contrast to most implementations of red-black trees, however, there is no pointer from a node to its parent. We are able to dispense with this (and so save some space) by implementing `insert` with the help of a _stack_ that keeps track of the relevant paths through the tree. The cost is a small increase in the runtime of `insert` . 

Type `Node(5,’five’)` to the Python prompt. You’ll see a readable representation of the node this has created, with the colour initialized to red. Note, however, that this representation isn’t itself a valid Python expression that could be used to construct a node. 

Near the end of the file, you will see some commands to construct a tree directly ‘by hand’. Typing `sampleTree` to the prompt will reveal a (semi-)readable representation of this tree, with subtrees indicated by square brackets. (Once again, this isn’t a valid Python expression.) Building trees directly in this way is useful for testing and debugging, but is of course ‘unsafe’ in that there’s nothing here to enforce the rules for red-black trees. The safe way will be to start from the empty tree (created by `RedBlackTree()` ) and repeatedly call the `insert` method, once you have implemented this. 

You can also type 

### `sampleTree.keysLtoR()` 

to compute a list of all the keys present, obtained by traversing the tree from left to right. 

Within the class `RedBlackTree` itself, study the provided code for the methods `repr` (which creates the readable representation) and `keysLtoR` . These provide examples of methods implemented using a recursive helper function: this is the pattern you should follow in your implementation of `lookup` and `insert` . 

**Task 1 (6 marks).** At the point marked `# TODO: Task 1` , implement a method 

```
lookup(self,key)
```

that returns the value associated with the given key (or `None` if this key is not present). The use of a helper method is encouraged: you may follow the example of the `contains` method from lectures. 

**Task 2 (12 marks).** At the point marked `# TODO: Task 2` , implement a method 

```
plainInsert(self,key,value)
```

that inserts a new key-value pair into the ordered tree at the correct position. The new node should be built using the `Node` constructor, which will initially colour it `Red` (and you should leave it like this). If the given key is already present in the tree, the method should simply overwrite the existing value with the one given — in this case it should not create a new node or make any other change to the tree. 

You may follow the example of the `insert` method for plain binary trees from lectures. The case of inserting into an initially empty tree will need special treatment. 


Once you have got the basic form of this method working, you should add suitable commands so that the path from the root to the new (or updated) node is recorded as a list in the `self.stack` field. Specifically, after calling the method, this field should contain the list of `Node` objects from the root to the new node, alternating with the special values `Left` and `Right` to indicate the branches chosen. (These are the possible values for the Python _enumeration type_ `Dir` , which is declared by the provided code.) For example, calling 

```
sampleTree.plainInsert(5,’five’)
sampleTree.showStack()
```

should result in the list 

```
[’2:two:B’,’r’,’4:four:R’,’r’,’6:six:B’,’l’,’5:five:R’]
```

Here, for convenience, the values `Left` and `Right` are _displayed as_ the strings `’l’` and `’r’` , but the values that your code puts in the stack should be the actual `Left` and `Right` as declared by the provided code. If the tree is initially empty, the stack after the insertion should contain just one node. 

Of course, the tree resulting from `plainInsert` may not be a legal red-black tree. The purpose of Tasks 3 and 4 is to do the fix-up needed to obtain a legal tree. 

**Task 3 (12 marks).** Here the task is to write code to apply the _red-uncle rule_ as many times as possible. 

By the _current node_ , we shall mean the one at the top (= right-hand end) of the stack. The red-uncle rule will be applicable if the current node, its parent and its uncle are all coloured red. In this situation, the rule may be applied by colour-flipping of nodes as described in the lecture. 

Write a method `tryRedUncle(self)` that first tests whether the conditions of the rule apply. If they don’t, the method should simply return `False` without making any changes. If they do, the method should apply the rule and return `True` . In the latter case, it should also remove some items from the stack as appropriate (using the `pop` method for lists) so that the new current node will be the one you have just coloured red. This will set things up correctly for the next attempt at the red-uncle rule. 

Here and in Task 4, you’re encouraged to use the provided operations `opposite` , `getChild` , `setChild` to reduce needless duplication within your code. Colours should always be represented by the values `Red` , `Black` of the provided enumeration type `Dir` . 

Now write a method `repeatRedUncle(self)` that uses `tryRedUncle` to apply the rule as many times as possible (which may be zero times). 

- **Task 4 (14 marks).** Once we have applied red-uncle as much as possible, we will be in one of the _endgame scenarios_ described in Lecture 9. Your main task here is to write a method `endgame(self)` that inspects the tree to see what needs to be done, and applies the appropriate action to turn it into a legal red-black tree. (You may assume that the stack is in the state in which is has been left by calling `repeatRedUncle` .) 

The provided functions `toNextBlackLevel` and `balancedTree` are there to help you in the case where some local re-balancing is called for. In other implementations (and e.g. in CLRS), this is achieved by means of certain _rotation_ operations, but here I’ve 


followed the more simple-minded approach of inspecting the relevant subtree down to the next ‘level of blacks’, retrieving the relevant 7 components A,a,B,b,C,c,D (in the notation of the lecture slides), and building a new and more ‘balanced’ subtree from these. Some inspection of the provided code may help you to understand what is going on. 

Now add a method `insert(self,key,value)` that pulls everything together, inserting the given key-value pair into the tree and performing all necessary fix-up. 

Up to 6 marks awarded for the correctness of `endgame` ; then up to a further 8 marks for everything working correctly together once the method `insert` is in place. 

- **The final 6 marks** for Part B will be awarded by the human marker for efficiency and code style. (Not that the autotests for Part B will not test for efficiency. However, in this case, it’s likely that any reasonable correct implementation will have the efficiency we expect.) 

You should test your code thoroughly to ensure that you’ve handled all cases correctly. One way to test it (though don’t rely exclusively on this) would be using the provided function `treeSort` , which uses a red-black tree to sort a given list in _O_ ( _n_ lg _n_ ) time. This isn’t a very serious contender for a sorting algorithm, though it’s somewhat reminiscent of the way HeapSort works. You might also like to do some experiments of your own to compare the efficiency of `treeSort` with that of `smartMergeSortAll` on lists of various kinds. 

## **Submission and autotest instructions** 

You should submit your work to **Gradescope** , using the Assessment _>_ Coursework 1 _>_ Gradescope link within the Inf2-IADS Learn page. Gradescope will be open for submission **from Friday 23 October** . The deadline is **12 noon on Friday 13 November** . Please submit your two completed files under the original filenames — `perfhash.py` and `redblack.py` — and do not attempt to submit any other files. 

You can re-submit as many times as you like up to the deadline — the last submission made before the deadline will be the one that is marked. **However,** if you do this, please ensure that you re-submit **both files** , not just the one that has changed! Only the files included in your most recent submission will be marked. 

Good luck!!! — John 

