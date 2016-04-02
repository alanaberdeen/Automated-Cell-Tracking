# Opto.py
# Optimisation setup and control


# Import
from pyomo.environ import *


def opto(a_coup, b_flow, c_cost):

    # opto
    # Function to set up the model and call the optimisation engine
    #
    # Inputs:   a_coup      -   coupled incidence matrix
    #           b_flow      -   sum of flow for each vertex
    #           c_cost      -   vector of edge costs
    #
    # Outputs:  sol         -   solution vector
    #

    # build model
    model = model_construct(a_coup, b_flow, c_cost)

    # solve
    sol = solve(model)

    return sol


def model_construct(a_coup, b_flow, c_cost):

    # construct pyomo model
    #
    # Inputs:   a_coup      -   coupled incidence matrix
    #           b_flow      -   sum of flow for each vertex
    #           c_cost      -   vector of edge costs
    #
    # Outputs:  model       -   pyomo model object

    # Creation of a Concrete Model
    model = ConcreteModel()

    # Define sets
    vertices = range(a_coup.shape[0])
    edges = range(a_coup.shape[1])
    model.i = Set(initialize=vertices, doc='vertices')
    model.j = Set(initialize=edges, doc='edges')

    # Define parameters
    # Table a(i,j)  coupled incidence matrix
    def a_init(model, i, j):
        return a_coup.item(i, j)
    model.a = Param(model.i, model.j, initialize=a_init,
                    doc='coupled incidence')

    # cost vector
    def c_init(model, j):
        return c_cost[j]
    model.c = Param(model.j, initialize=c_init, doc='cost vector')

    # flow vector
    def b_init(model, i):
        return b_flow[i]
    model.b = Param(model.i, initialize=b_init, doc='flow vector')

    # Define variables
    model.x = Var(model.j, domain=Binary,
                  doc='solution vector 1 if column is included 0 otherwise')

    # Define constraints - slightly modified from paper because no source/sink
    def flow_rule(model, i):
        # for the L and R cells we need to ensure exact flow
        if -1 <= model.b[i] <= 1:
            flow = sum(model.a[i, j]*model.x[j] for j in model.j) == model.b[i]
        # otherwise we can be more flexible
        else:
            flow = sum(model.a[i, j]*model.x[j] for j in model.j) <= model.b[i]
        return flow

    model.constrain = Constraint(model.i, rule=flow_rule,
                                 doc='Flow Constraints')

    # Define Objective
    obj_expr = sum(model.c[j]*model.x[j] for j in model.j)
    model.objective = Objective(expr=obj_expr, sense=minimize,
                                doc='Define objective function')

    return model


def solve(model):

    # solve
    # calls the GLPK solver and finds solution
    #
    # Inputs:   model   -   Pyomo model object
    # Outputs:  x       -   binary |E|x1 solution vector that is 1 if the
    #                       row is in the solution and 0 otherwise.

    # This is an optional code path that allows the script to be
    # run outside of Pyomo command-line.  For example:  python transport.py
    # This replicates what the Pyomo command-line tools does
    from pyomo.opt import SolverFactory
    opt = SolverFactory("glpk")
    results = opt.solve(model)

    # save results
    model.solutions.load_from(results)
    x = model.x._data

    return x
