from ortools.sat.python import cp_model
import random; random.seed(42)
from time import time

# init the problem variables
lb, ub = 0, 100
n = 20
k = 5
arr = [random.randint(lb, ub) for _ in range(n)]

print('Problem Description:')
print('Find {} values from {} such that the sum of the k values is maximum'.format(k, arr))
'''Find 3 values from [81, 14, 3, 94, 35, 31, 28, 17, 94, 13] such that the sum of the k values is maximum'''
print('----------------------------------------------------')

# init the model
#region
model = cp_model.CpModel()

# create k variables
k_arr = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(arr), 'k_%i' % i) for i in range(k)]

# add the constraints
model.AddAllDifferent(k_arr)
# model.AddDecisionStrategy(k_arr, cp_model.CHOOSE_FIRST, cp_model.SELECT_MAX_VALUE)
model.Maximize(sum(k_arr))
#endregion

# init the solver and solve the model
solver = cp_model.CpSolver()
time_start = time()
status = solver.Solve(model)
time_end = time()

print('Solution: {} with sum = {}\nSolved in {}'.format([solver.Value(k_arr[i]) for i in range(k)], solver.ObjectiveValue(), time_end - time_start))