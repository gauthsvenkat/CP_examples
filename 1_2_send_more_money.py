'''
     S E N D
   + M O R E
  ----------
 = M O N E Y 
  ----------
'''

from ortools.sat.python import cp_model

# Class whose object will be passed as a callback to the solver.
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s=%i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count 

# init the model
model = cp_model.CpModel()
base = 10

# create the variables
s = model.NewIntVar(0, base - 1, 's')
e = model.NewIntVar(0, base - 1, 'e')
n = model.NewIntVar(0, base - 1, 'n')
d = model.NewIntVar(0, base - 1, 'd')
m = model.NewIntVar(0, base - 1, 'm')
o = model.NewIntVar(0, base - 1, 'o')
r = model.NewIntVar(0, base - 1, 'r')
y = model.NewIntVar(0, base - 1, 'y')

variables = [s, e, n, d, m, o, r, y]

# add the constraints
model.Add(
                    (base**3) * s + (base**2) * e + (base**1) * n + (base**0) * d 
                    +
                    (base**3) * m + (base**2) * o + (base**1) * r + (base**0) * e 
                    ==
    (base**4) * m + (base**3) * o + (base**2) * n + (base**1) * e + (base**0) * y
)

model.AddAllDifferent(variables)

# init the solution printer object
solution_printer = VarArraySolutionPrinter(variables)

# init the solver and pass the solution printer object as a callback
solver = cp_model.CpSolver()
status = solver.SearchForAllSolutions(model, solution_printer)

print('Number of satisfiable solutions : %i' % solution_printer.solution_count())
