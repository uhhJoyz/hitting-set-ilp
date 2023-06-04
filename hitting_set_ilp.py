"""
A solver for the hitting set problem.
"""
__author__ = "William Bradford"
__email__ = "wcb8ze@virginia.edu"

import gurobipy as gp
from gurobipy import LinExpr


def write_from_sets(sets, filepath):
    """
    A function that takes a list of sets and a name and writes the sets to a text file in the form of an ILP
    :param sets: List<List<int>> : a list of sets
    :param filepath: String : a name for a file without a file extension
    :return: void
    """
    # create a universe, include repeated items
    u = []
    for s in sets:
        # add each set to the universe
        u += s
    # make the universe a range between 1 and the highest value in the universe
    u = range(1, max(u)+1)

    # initialize an empty B matrix
    B = [[0 for i in range(len(u))] for i in range(len(sets))]
    # for each set
    for (i, s) in enumerate(sets):
        # for eat item in the set
        for (j, item) in enumerate(s):
            # write the item to the B matrix
            B[i][item - 1] = 1

    # create the first row of the output
    output = f"{len(sets)} {len(u)} \n"
    # for each row in the B matrix
    for (idx, row) in enumerate(B):
        # append the number corresponding to the data item
        output += f"{idx + 1} "
        # for each item in the row
        for item in row:
            # append the item to the string
            output += f"{item} "
        # append a newline character if the current line is not the last
        if idx != len(B) - 1:
            output += "\n"

    # create/open a file with the specified name
    with open(f"{filepath}.txt", "w") as f:
        # write the output string to that file
        f.write(output)


def from_sets(sets):
    """
    A function to calculate the hitting set
    :param sets: List<List<int>> : the sets of the hitting set problem
    :return: List<int> : the minimum tags required to cover the sets
    """
    # create a universe, include repeated items
    u = []
    for s in sets:
        # add each set to the universe
        u += s
    # cast the universe to a set, then cast it back to a list to remove duplicates
    u = range(1, max(u)+1)
    return from_universe_sets(u, sets)


def from_universe_sets(universe, sets):
    """
    Calculate the hitting set problem from a universe and a list of sets
    :param universe: List<int> : the universe containing all tags
    :param sets: List<List<int>> : the sets
    :return: List<int> : the minimum tags required to cover the sets
    """
    # initialize an empty B matrix
    B = [[0 for i in range(len(universe))] for i in range(len(sets))]
    # for each set
    for (i, s) in enumerate(sets):
        # for each item in the set
        for (j, item) in enumerate(s):
            # write the item to the B matrix
            B[i][item-1] = 1

    return hitting_set_ilp(len(sets), len(universe), B)


def solve(filepath):
    """
    The solver function. Takes in a hitting set problem as specified by the ILP reduction, outputs the minimum number of tags
    required to hit each of the sets at least once.
    :param filepath: string : the path to the corresponding ILP formulation of the hitting set problem
    :return: List<int> : the minimum tags required to hit all the sets
    """
    # open the input file
    with open(filepath) as f:
        # read it
        input = f.read()

    # remove newline characters
    input.replace("\n", "")
    # split the input array on spaces
    input_array = input.split()
    # obtain the n value
    n = int(input_array[0])
    # obtain the t value
    t = int(input_array[1])
    # remove the n and t values from the input file
    input_array = input_array[2:]

    # create an empty B matrix
    B = []
    # for each data item
    for i in range(n):
        # append an empty list
        B.append([])
        # for each tag
        for j in range(i+1, t+i+1):
            # append the data from each data item
            B[i].append(int(input_array[(i * t) + j]))

    return hitting_set_ilp(n, t, B)


def hitting_set_ilp(n, t, B):
    """
    A helper function that takes in the number of data items, followed by the number of sets,
    followed by the resulting B matrix and returns the solution to the corresponding minimum hitting set problem
    :param n: int : the number of data items
    :param t: int : the number of sets
    :param B: List<List<int>> : the B matrix from the hitting set problem
    :return: List<int> : the minimum tags required to hit items in the universal set
    """
    # set an empty environment
    with gp.Env(empty=True) as env:
        # set the env output flag to zero to suppress console output
        env.setParam('OutputFlag', 0)
        # start the environment
        env.start()
        # create the model in the console-suppressed environment
        with gp.Model(env=env) as m:
            # create a list of the y_j variables
            y_var = [m.addVar(vtype=gp.GRB.BINARY, name=f"y{i}") for i in range(1, t + 1)]

            # create a list of 1's to set up the LinExpr with
            coef = [1 for j in range(t)]

            # set the model objective to minimize the number of y_j values that are 1
            m.setObjective(LinExpr(coef, y_var), gp.GRB.MINIMIZE)
            # update the model
            m.update()

            # create an empty list of constraints to add
            c = [0 for i in range(n+1)]
            # for each data item
            for i in range(1, n + 1):
                # for each tag
                for j in range(1, t+1):
                    # if the corresponding value of the B matrix is 1
                    if B[i-1][j-1] == 1:
                        # add the variable to the sum at position i
                        c[i] += y_var[j-1]
                # set the constraint that the sum at index i must be >= 1
                m.addLConstr(c[i], ">=", 1)
            # update the model
            m.update()
            # optimize the model
            m.optimize()

            # get the values of variables
            x_values = m.getAttr("X")
            
            # initialize an empty list 
            desc = []
            # for each variable
            for (i, x) in enumerate(x_values):
                # if the variable is set to 1
                if x == 1:
                    # append it to the descriptor
                    desc.append(i+1)
    return desc
