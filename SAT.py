import random
import sys
import time

num_variables = int()
num_clauses = int()
backtrack = 0


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
    dict = {}
    for clause in formula:
        for literal in clause:
            if literal in dict:
                dict[literal] += 1
            else:
                dict[literal] = 1
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    dict = dict[0][0]
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
    dict = dict[0][0]
    return dict

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
        '-S1'    : dlis,
        '-S2'   : jeroslow,
        '-S3'    : mom,
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

def dpll(formula, assignment, heuristic):

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

#    formula, pure_assign = pure_(formula)
#    assignment = assignment + pure_assign
#    #if bcp found inconsistency, variable assignment is not an potential solution
#    if formula == - 1:
#        return []
#
#    #if all clauses satisfied
#    if not formula:
#        return assignment

    #choose which variable should be explored first (no heuristic yet) creates a dictionary with key = literal and value = counted times in formula
    variable = heuristic(formula)
    potential_assignment = assignment + [variable]
    solution = dpll(boolean_constraint_propagation(formula, variable), potential_assignment,heuristic)

    # if literal assignment of chosen variable did not satisfy then try -assignment for the variable
    if not solution:
        global backtrack
        backtrack += 1
        potential_assignment = assignment + [-variable]
        solution = dpll(boolean_constraint_propagation(formula, -variable), potential_assignment,heuristic)

    return solution


def write_output(sol,name):
    n_clause = len(sol)

    output = open(f'{name}.out', 'w')
    output.write(f"p cnf {n_clause} {n_clause} \n ")
    for element in sol:
        output.write(str(element) + ' 0 \n')
    output.close()


def run_sudoku(cnf,heuristic,name):
    solution = dpll(cnf, [], heuristic)
    if solution:
        solution.sort(key=abs)
        write_output(solution,name)

    else:
        print("unsolvable")

    return

def main():
    #SAT Sn inputfile , for example: SAT -S2 sudoku_nr_10 , where SAT is the (compulsory) name of your program,
    # n=1 for the basic DP and n=2 or 3 for your two other strategies,
    # and the input file is the concatenation of all required input clauses (in your case: sudoku rules + given puzzle).

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.exit("Use: python SAT -Sn <path_to_inputfile.txt> (with n =1 for DPLL n=2 for Jeroslow n=3 for MOM)  ")
    if sys.argv[1][0] == "-" and sys.argv[1][1] == "S":
        try:
            heuristic = heuristics_dict(sys.argv[1])
        except:
            print("Use 1, 2 or 3 for n in '-Sn' ")
        if len(sys.argv) == 3:
            heuristic = heuristics_dict(sys.argv[1])
        file = sys.argv[2]
        file = file[:-4]
        cnf, n_variable, n_clauses = parse(sys.argv[2])
        run_sudoku(cnf,heuristic,file)


if __name__ == '__main__':
    main()