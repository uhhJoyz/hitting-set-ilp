# Hitting Set ILP

A set of methods for solving the minimum hitting set problem using integer linear programming.
Documentation is available in docs.md as well as being found in the code itself. The code is 
thoroughly commented, so feel free to read through it if any part of the function of this program
is unclear.

The ILP formation of this minimum hitting set algorithm can be stored in a text file using the following formatting:
- One number representing n
- Another number representing t
- The B matrix of your problem, with the data item's number at the beginning of the line

Example:

    5 4
    1 0 0 0 1
    2 0 1 1 0
    3 0 0 1 0
    4 0 1 0 0
    5 1 0 0 0

This problem corresponds to the following sets, with 5 sets and 4 tags:
- [4]
- [2, 3]
- [3]
- [2]
- [1]

The solution to this problem is [1, 2, 3, 4]. Each data item corresponds to a set, represented with 1's at the location of each tag contained within the sets.  