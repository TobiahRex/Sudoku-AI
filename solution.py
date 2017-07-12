assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
from collections import defaultdict


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values



def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    twins_dict = {} # dictionary that contains all the naked twins in the puzzle
                    # example is ('B7', 'A7'): {'2', '7'}
    for unit in unitlist: # move through the unit lists 
        pairs = {box:values[box] for box in unit if len(values[box]) == 2} # contains the cells which are candidates for twin pairs
        pairs = {p: set(values[p]) for p in pairs} # convert the values to a set since the order doesn't matter 
        naked_twins = {} # reduce the set of candidate twin pairs to the set of all naked twins 
        for key,value in pairs.items(): 
            match = [k for (k, v) in pairs.items() if v == value and k != key] # checking to see if a twin exists! 
            if match: # a match exists iff there exists the same value with a different key! 
                naked_twins[match[0]] = value
        # We now merge the keys of the dictionary with common values into a tuple
        # For example, if naked_twins = {'E2': {'5', '7'}, 'E3': {'4', '8'}, 'E5': {'5', '7'}, 'E8': {'4', '8'}}
        # Then the output (twins_merge) should look like =  {('E2', 'E5'): {'5', '7'}, ('E3', 'E8'): {'4', '8'}}
        naked_twins_temp = defaultdict(list) # Store the naked twins in a list 
        for a, b in naked_twins.items():
            naked_twins_temp[tuple(b)].append(a)
        twins_merge = {tuple(b): set(a) for a, b in naked_twins_temp.items()}
        twins_dict.update(twins_merge) # Update the full dictionary of all naked twins in the puzzle 

    # Eliminate the naked twins as possibilities for their peers
    for twins, v in twins_dict.items():
        v = list(v) # convert from set to list 
        # We now compute the candidates that may contain values that we can eliminate
        eliminate_candidates = [set(peers[twins[0]]).intersection(peers[twins[1]])][0]
        for e in eliminate_candidates:
            if v[0] in values[e]: # check if the younger twin can be crossed out 
                values = assign_value(values, e, values[e].replace(v[0], ''))
            if v[1] in values[e]: # check if the older twin can be crossed out 
                values = assign_value(values, e, values[e].replace(v[1], ''))
    return values 

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#NB: Add the diagonal units to the unitlist as an added constraint to the puzzle 
diag_units = [[rs+cs for (rs,cs) in zip(rows, cols)], [rs+cs for (rs,cs) in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for u in unitlist:
        firstSeen = {}
        seen = []
        seenAlready = []
        for cell in u:
            if len(values[cell]) > 1:
                for num in values[cell]:
                    if num not in seen: # first time seeing value
                        seen.append(num)
                        firstSeen[num] = cell
                    else: # already seen
                        if num not in seenAlready: # only care if the val was seen more than onnce
                            seenAlready.append(num)
        for seen_value in seen:
            if seen_value not in seenAlready and seen_value not in [i for i in list({k: values[k] for k in u}.values()) if len(i)==1]:
                #print(firstSeen[seen_value], seen_value)
                values = assign_value(values, firstSeen[seen_value], seen_value)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy 
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    #print('New Call')
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        #print("Values is False")
        return False
    if all(i==1 for i in [len(values[k]) for k in values]):
        #print('Done!!!')
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    candidate_squares = {key : len(value) for (key, value) in values.items() if len(value)>1}
    square_min = min(candidate_squares, key=candidate_squares.get)
    childQueue = [] # Create a queue of children puzzle 
    for num in values[square_min]:
        childDict = {k:v for k, v in values.items()}
        childDict = assign_value(childDict, square_min, num)
        childQueue.append([childDict, [square_min, num]])
        
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for child, change in childQueue:
        #print(change[0], change[1], 'from', values[square_min])
        solution = search(child)
        if solution != False: # if a child is not False, it might be able to be solved 
            # This child is possibly solvable 
            return solution
    # if we make it thru the for loop then every child is False, which means we can prune that section of the tree
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid_values(diag_sudoku_grid)
    
    display(solve(diag_sudoku_grid))

#
#    try:
#        from visualize import visualize_assignments
#        visualize_assignments(assignments)
#
#    except SystemExit:
#        pass
#    except:
#        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
