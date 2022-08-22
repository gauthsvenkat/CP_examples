from ortools.sat.python import cp_model
import numpy as np

def generate_sudoku(n, proportion_empty=0.25, seed=42):

    np.random.seed(seed)

    model = cp_model.CpModel()

    cells = np.array([[
                model.NewIntVar(1, n, 'cell_%i_%i'%(i+1, j+1)) 
                for j in range(n)
            ]   for i in range(n)
        ]
    )

    for i in range(n):
        model.AddAllDifferent(cells[i])
        model.AddAllDifferent(cells[:,i])
    
    grid_length = int(np.sqrt(n))
    for i in range(0, n, grid_length):
        for j in range(0, n, grid_length):
            model.AddAllDifferent(cells[i:i+grid_length,j:j+grid_length].reshape(-1))

    solver = cp_model.CpSolver(); solver.parameters.random_seed = seed; 
    _ = solver.Solve(model)

    full_sudoku = np.vectorize(solver.Value)(cells)
    mask = np.random.choice([0, 1], size=(n, n), p=[proportion_empty, 1-proportion_empty])

    return full_sudoku * mask

def display_sudoku(sudoku):
    n = len(sudoku)
    grid_length = int(np.sqrt(n))
    for i in range(0, n):
        if i!=0 and i % grid_length == 0:
            print('+'.join(['-'*(grid_length*3)]*grid_length))
        for j in range(0, n):
            if j!=0 and j % grid_length == 0:
                print('|', end='')
            if sudoku[i,j] == 0:
                print('{:>2}'.format('-'), end=' ')
            else:
                print('{:>2}'.format(sudoku[i,j]), end=' ')
        print('')

# init the problem variables
n = 9
seed = 42
sudoku = generate_sudoku(n)

print('Sudoku:')
display_sudoku(sudoku)
'''
 9  8  7 | 6  -  - | -  2  1 
 6  -  3 | 9  -  - | -  7  5 
 5  2  1 | -  7  3 | 9  6  - 
---------+---------+---------
 7  9  - | 4  -  - | 2  1  8 
 8  -  5 | 1  -  2 | -  4  6 
 4  1  2 | 7  -  8 | 5  9  3 
---------+---------+---------
 3  7  - | -  -  6 | 1  8  2 
 2  6  8 | -  1  - | 4  5  - 
 -  5  4 | 2  8  - | 6  -  9 
'''
print('\n\n')

#region
model = cp_model.CpModel()

# create the variables (2d array of variables)
cells = np.array([[
            model.NewIntVar(1, n, 'cell_%i_%i'%(i+1, j+1)) 
            for j in range(n)
        ]   for i in range(n)
    ]
)

# initialize the non-empty cells
_ = [model.Add(cells[i,j] == sudoku[i,j]) for i in range(n) for j in range(n) if sudoku[i,j] != 0]

# add the row and columns constraints
for i in range(n):
    model.AddAllDifferent(cells[i]) # all different row
    model.AddAllDifferent(cells[:,i]) # all different column

# add the grid constraints
grid_length = int(np.sqrt(n))
for i in range(0, n, grid_length):
    for j in range(0, n, grid_length):
        model.AddAllDifferent(cells[i:i+grid_length,j:j+grid_length].reshape(-1))
#endregion

solver = cp_model.CpSolver(); solver.parameters.random_seed = seed; 
_ = solver.Solve(model)
solution = np.vectorize(solver.Value)(cells)

print('Solution:')
display_sudoku(solution)
