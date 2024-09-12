import numpy as np
from scipy.optimize import linprog

def incremental_lp_solver(c, A_ub, b_ub, d):
    n_constraints = len(A_ub)
    
    # Find the first partial solution x*_{d+1}
    res = linprog(c, A_ub=A_ub[:d+1], b_ub=b_ub[:d+1], bounds=[(0, None), (0, None)], method='highs')
    if not res.success:
        return None, None, False

    x_star = res.x
    
    # Incrementally add constraints
    for i in range(d+2, n_constraints+1):
        if np.all(A_ub[i-1] @ x_star <= b_ub[i-1]):
            # Case 1: x*_{i-1} satisfies the constraint H_i(x), so x*_i = x*_{i-1}
            continue

        else:
            # Case 2: Calculate x*_i with updated constraints
            # Solve the problem using d-1 variables and constraints
            # that H'j is the join of Hj and Hi
            combined_A_ub = np.vstack([A_ub[:i-1], A_ub[i-1]])
            combined_b_ub = np.hstack([b_ub[:i-1], b_ub[i-1]])

            res = incremental_lp_solver(c, combined_A_ub, combined_b_ub, d-1)
            if not res.success:
                return None, None, False
            x_star = res.x
    
    return res.fun, x_star, True

'''
Problem : maximize{-3x1 + 12x2} ---> Objective Function

Constraints :  x1 - 2x2 >=1
              2x1 - 3x2 >= 6
              -x1 + 3x2 <= 0
              -x1 + 6x2 <= 12
              4x1 - 9x2 <= 27
               x1, x2   >= 0

In order to solve this problem with SciPy library and linprog method
we need to transfrom it into a minimization problem, because linprog 
solves only minimization problems. We know that: max{f(x)} = -min{-f(x)}
So, the problems comes to:

Problem : minimize{-(-3x1 + 12x2)} = min{3x1 - 12x2} ---> Objective Function

Constraints :  -x1 + 2x2 <= -1
              -2x1 + 3x2 <= -6
              -x1  + 3x2 <=  0
              -x1 + 6x2 <=  12
              4x1 - 9x2 <=  27
               x1, x2   >=  0

We change the order in order to let linprog from SciPy to find the first
optimal solution for d+1 constraints. So, we have :

Constraints : -x1  + 3x2 <=  0
              -x1 + 6x2 <=  12
              4x1 - 9x2 <=  27
              -x1 + 2x2 <= -1
              -2x1 + 3x2 <= -6
               x1, x2   >=  0

'''
if __name__ == "__main__":

    # Coefficients for the objective function
    c = [3, -12]

    # Coefficients for the inequality constraints
    A_ub = [
        [-1, 3],
        [-1, 6],
        [4, -9],
        [-1, 2],
        [-2, 3]
    ]

    # Right-hand side values for the inequality constraints
    b_ub = [
             0,
            12,
            27,
            -1,
            -6
        ]

    d = 2  # Number of initial constraints to consider

    opt_val, x_opt, success = incremental_lp_solver(c, A_ub, b_ub, d)
    if success:
        print("Optimal value: ", -opt_val)
        print("Optimal solution found:", x_opt)
    else:
        print("No solution found")
