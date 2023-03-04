import random
import sys
import time
import pandas as pd

num_variables = int()
num_clauses = int()
count= 0
backtrack = 0
ALGORITHM = 'Normal DPLL'

def load_txt16(data): # transform a sudoku into cnf
    cnf = []
    for i in range(1, 17):
        for j in range(1, 17):
            if data[0] != '.':
                if (data[0] == 'G'):
                    d = 16
                else:
                    d = int(data[0], 16)
                cnf.append([i*17*17 + j*17 + d])
            #print(i, j)
            #print(i*17*17 + j*17 + d)
            data = data[1:]
    return cnf

def load_txt9(data): # transform a sudoku into cnf
    cnf = []
    for i in range(1, 10):
        for j in range(1, 10):
            if data[0] != '.':
                d = int(data[0])
                cnf.append([i*10*10 + j*10 + d])
            data = data[1:]
    return cnf

def load_txt4(data): # transform a sudoku into cnf
    cnf = []
    for i in range(1, 5):
        for j in range(1, 5):
            if data[0] != '.':
                d = int(data[0])
                cnf.append([i*10*10 + j*10 + d])
            data = data[1:]
    return cnf


def load_dimacs(file):
    f = open(file, 'r') # open file in reading mode
    data = f.read() # read file in data variable; string type
    f.close()
    lines = data.split("\n") # split the data into a list of lines
    cnf = []
    for line in lines:
        if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
            continue # ignore the lines without clauses
        clause = [int(x) for x in line.split()[:-1]] # transform the string clause format into a int one, remove the last 0;
        cnf.append(clause) # add the clause to the list
    return cnf

def write_sudoku(solution):
    new= []
    for assignment in solution:
        if assignment < 0:
            continue
        new.append(assignment)
    col = 1
    for assignment in new:
        if col == 10:
            print("")
            col = 1
        print(f"{assignment % 10} ", end='')
        col += 1


def dict_literal(formula):
    dict = {}
    for clause in formula:
        for literal in clause:
            if literal in dict:
                dict[literal] += 1
            else:
                dict[literal] = 1
    return dict

def dlis(formula):
    dict = dict_literal(formula)
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    clause = random.choice(dict)
    dict = clause[0]
    return dict

def jeroslow(formula):
    dict = {}
    for clause in formula:
        for literal in clause:
            if literal in dict:
                dict[literal] += 2^(-abs(len(clause)))
            else:
                dict[literal] = 2^(-abs(len(clause)))
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return dict[0][0]


def mom(formula):
    min_len = min(map(len, formula))
    app = {}
    for clause in formula:
        if len(clause) == min_len:
            for literal in clause:
                if literal in app:
                    app[literal] += 1
                else:
                    app[literal] = 1
    mom_value_max = 0
    keys = app.keys()
    for i in keys:
        try:
            mom_value_new = (app.get(i) + app.get(-i))*2 + app.get(i) + app.get(-i)
            if mom_value_new > mom_value_max:
                mom_value_max = mom_value_new
                mom_best = i
        except:
            continue
    return mom_best

def heuristics_dict(heuristic):
    heuristics = {
        'S1'    : dlis,
        'S2'   : jeroslow,
        'S3'    : mom,
    }
    try:
        return heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Not valid heuristic.".format(heuristic) +
                 "\nValid heuristics: {}".format(heuristics.keys()))

def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            n_vars = line.split()[2]
            num_clauses= line.split()[3]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses, int(n_vars), int(num_clauses)

def boolean_constraint_propagation(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified

def unit_propagation(formula):
    assignment = []
    unit_clauses = []
    for clause in formula:
        if len(clause) == 1:
            unit_clauses.append(clause)

    while unit_clauses:

        unit = unit_clauses[0]

        formula = boolean_constraint_propagation(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = []
        for clause in formula:
            if len(clause) == 1:
                unit_clauses.append(clause)
    return formula, assignment


def pure_(formula):
    dict= dict_literal(formula)
    keys = dict.keys()
    pures = []
    assignment = []
    for key in keys:
        if -key in keys:
            continue
        else:
            pures.append(key)
    while pures:
        pure = pures[0]
        formula = boolean_constraint_propagation(formula, pures[0])
        assignment += [pure[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        pures = []
        for key in keys:
            if -key in keys:
                continue
            else:
                pures.append(key)
    return formula, assignment

def dpll(formula, assignment,heuristic):

    #unit_clauses
    formula, unit_assignment = unit_propagation(formula)
    #add all assignment from unit_clauses to solution assignment

    assignment = assignment + unit_assignment
    #if bcp found inconsistency, variable assignment is not an potential solution
    if formula == - 1:
        return []

    #if all clauses satisfied
    if not formula:
        return assignment

  # formula, pure_assign = pure_(formula)
  # assignment = assignment + pure_assign
  # #if bcp found inconsistency, variable assignment is not an potential solution
  # if formula == - 1:
  #     return []

  # #if all clauses satisfied
  # if not formula:
  #     return assignment

    #choose which variable should be explored first (no heuristic yet) creates a dictionary with key = literal and value = counted times in formula
    variable = heuristic(formula)
    potential_assignment = assignment + [variable]
    solution = dpll(boolean_constraint_propagation(formula, variable), potential_assignment,heuristic)

    # if literal assignment of chosen variable did not satisfy then try -assignment for the variable
    if not solution:
        global backtrack
        backtrack += 1
        potential_assignment = assignment + [-variable]
        solution  = dpll(boolean_constraint_propagation(formula, -variable), potential_assignment,heuristic)
    return solution


def run_sudoku(cnf,heuristic):
    start_time = time.time()
    solution = dpll(cnf, [],heuristic)
    end_time = time.time() - start_time
    global backtrack
    bk = backtrack
    backtrack = 0
    if solution:
        solution.sort(key=abs)
        # write_sudoku(solution)
        success = 1
    else:
        success = 0

    return end_time, success, bk

def experiment(heuristickey):
    heuristic = heuristics_dict(heuristickey)
    total_runtime = 0
    total_success = 0
    total_unit_clauses = 0
    total_backtracks = 0
    size = 0
    num_list = []
    success_list = []
    runtime_list = []
    backtrack_list = []
    sudoku_list = []
    size_list = []

    with open('sudokus/1000 sudokus.txt') as file:
        for line in file:
            if len(line) == 0:
                continue
            if len(line) == 82:
                line =  line[:-1]
            sudoku_list.append(line)

    with open('sudokus/16x16.txt') as file:
        for line in file:
            if len(line) == 0:
                continue
            if len(line) == 257:
                line = line[:-1]
            sudoku_list.append(line)
    with open('sudokus/4x4.txt') as file:
        for line in file:
            if len(line) == 0:
               continue
            if len(line) == 17:
               line = line[:-1]
            if len(line) == 16:
               sudoku_list.append(line)

# HERE CAN YOU DETERMINE HOW MANY SUDOKUS TO PUT IN THE CSV
    for i in range(len(sudoku_list)):
        if len(sudoku_list[i]) == 256:
            size_list.append(16)
            sudoku = load_txt16(sudoku_list[i])
            rules = load_dimacs('sudokus/sudoku-rules-16x16.txt')
            cnf = sudoku + rules
        if len(sudoku_list[i]) == 81:
            size_list.append(9)
            sudoku = load_txt9(sudoku_list[i])
            rules = load_dimacs('sudokus/sudoku-rules.txt')
            cnf = sudoku + rules
        if len(sudoku_list[i]) == 16:
            size_list.append(4)
            sudoku = load_txt4(sudoku_list[i])
            rules = load_dimacs('sudokus/sudoku-rules-4x4.txt')
            cnf = sudoku + rules
        runtime, success, backtrack = run_sudoku(cnf,heuristic)
     #   total_unit_clauses = + unit_clauses
        total_runtime += runtime
        total_success += success
        total_backtracks += backtrack

        num_list.append(sudoku_list[i])
        success_list.append(success)
        runtime_list.append(runtime)
        backtrack_list.append(backtrack)
        average_backtrack = total_backtracks / len(sudoku_list)
        success_ratio = total_success / len(sudoku_list)
    if heuristickey == "S1":
        ALGORITHM = "DPLL1"
    if heuristickey == "S2":
        ALGORITHM = "Jeroslow1"
    if heuristickey == "S3":
        ALGORITHM = "MOM1"
    if heuristickey == "S4":
        ALGORITHM = "JWQuick"
    print('Time elapsed: ', total_runtime, 'Success: ', total_success)
    sudokuframe = pd.DataFrame(
        {'num': num_list, 'runtime': runtime_list, 'success': success_list, "number of backtracks": backtrack_list,"size" : size_list, "heuristics": ALGORITHM})
    sudokuframe.to_csv(f'{ALGORITHM}.csv')


experiment("S1")
experiment("S2")
experiment("S3")


