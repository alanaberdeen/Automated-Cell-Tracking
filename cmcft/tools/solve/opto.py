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
    # Output:   x - binary |E|x1 solution vector that is 1 if the row is in
    #               the solution and 0 otherwise.
    #

    # Creation of a Concrete Model
    model = ConcreteModel()

    # Define sets
    vertices = range(a_coup.shape[0])
    edges = range(a_coup.shape[1])
    model.i = Set(initialize=vertices, doc='vertices')
    model.j = Set(initialize=edges, doc='edges')

    # Define parameters
    # Table a(i,j)  coupled incidence matrix
    incidence = {}
    for row in xrange(a_coup.shape[0]):
        for column in xrange(a_coup.shape[1]):
            incidence[(row, column)] = a_coup.item((row, column))

    model.a = Param(model.i, model.j, initialize=incidence,
                    doc='coupled incidence')

    # cost vector
    costs = {}
    for index, value in enumerate(c_cost):
        costs[index] = value
    model.c = Param(model.j, initialize=costs, doc='cost vector')

    # flow vector
    flow = {}
    for index, value in enumerate(b_flow):
        flow[index] = value
    model.b = Param(model.i, initialize=flow, doc='flow vector')

    # Define variables
    model.x = Var(model.j, domain=Binary,
                  doc='solution vector 1 if column is included 0 otherwise')

    # Define constraints
    def flow_rule(model, i):
        return sum(model.a[i, j]*model.x[j] for j in model.j) <= model.b[i]
    model.constrain = Constraint(model.i, rule=flow_rule,
                                 doc='Flow Constraints')

    # Define Objective
    def objective_rule(model):
        return sum(model.c[j]*model.x[j] for j in model.j)
    model.objective = Objective(rule=objective_rule, sense=minimize,
                                doc='Define objective function')

    # Display of the output
    # Display x.l, x.m ;
    # def pyomo_postprocess(options=None, instance=None, results=None):
        #model.x.display()

    # This is an optional code path that allows the script to be
    # run outside of pyomo command-line.  For example:  python transport.py
    # This replicates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    opt = SolverFactory("glpk")
    results = opt.solve(model)

    # sends results to stdout
    #results.write()
    #pyomo_postprocess(None, instance, results)

    # save results
    model.solutions.load_from(results)
    x = model.x._data

    return x