'''
     S E N D
   + M O R E
  ----------
 = M O N E Y 
  ----------
'''

from ortools.sat.python import cp_model

# init the model
model = cp_model.CpModel()

# create the variables
s = model.NewIntVar(1, 9, 's') # sus
e = model.NewIntVar(0, 9, 'e')
n = model.NewIntVar(0, 9, 'n')
d = model.NewIntVar(0, 9, 'd')
m = model.NewIntVar(1, 9, 'm') # sus
o = model.NewIntVar(0, 9, 'o')
r = model.NewIntVar(0, 9, 'r')
y = model.NewIntVar(0, 9, 'y')

# add the constraints
model.Add(
                    1000 * s + 100 * e + 10 * n +  d 
                    +
                    1000 * m + 100 * o + 10 * r +  e 
                    ==
        10000 * m + 1000 * o + 100 * n + 10 * e +  y
)
#region
model.AddAllDifferent([s, e, n, d, m, o, r, y])
#endregion
# init the solver and pass the solution printer object as a callback
solver = cp_model.CpSolver()
_ = solver.Solve(model)

print('     {} {} {} {}'.format(solver.Value(s), solver.Value(e), solver.Value(n), solver.Value(d)))
print('   + {} {} {} {}'.format(solver.Value(m), solver.Value(o), solver.Value(r), solver.Value(e)))
print('  ----------')
print(' = {} {} {} {} {}'.format(solver.Value(m), solver.Value(o), solver.Value(n), solver.Value(e), solver.Value(y)))
print('  ----------')
