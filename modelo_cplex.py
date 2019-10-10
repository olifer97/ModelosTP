# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2015, 2018
# --------------------------------------------------------------------------

# The goal of the diet problem is to select a set of foods that satisfies
# a set of daily nutritional requirements at minimal cost.
# Source of data: http://www.neos-guide.org/content/diet-problem-solver

from collections import namedtuple

from docplex.mp.model import Model
from docplex.util.environment import get_environment

import csv

# ---------------------------------------------------------------------------
# Get data from csv
# ---------------------------------------------------------------------------

def get_distances_matrix():
    matrix = []
    with open("distancias_matrix.csv") as distancesFile:
        distancesCSV = csv.reader(distancesFile, delimiter=',')
        for distancesVotant in distancesCSV:
            matrix.append(distancesVotant)
    return matrix

def get_max_votants_centers():
    dic = {}
    with open("centros_reducido.csv") as centersFile:
        centersCSV = csv.reader(centersFile, delimiter=',')
        next(centersCSV, None)
        for center in centersCSV:
            if len(center) == 0: break
            dic[int(center[0])] = int(center[3]) #diccionario de la forma idCentro: maxCupo
    return dic


# ----------------------------------------------------------------------------
# Build the model
# ----------------------------------------------------------------------------

def build_diet_model(matrix, max_votants, min_votants, N, C):

    centers = range(1, C + 1) # TODOS LOS CENTROS
    votants = range(1, N + 1) # TODOS LOS VOTANTES


    # Model
    m = Model(name="Asignacion de centros de votacion")

    ## VARIABLES

    # Xij votante i asignado al centro j
    x = {(i,j): m.binary_var(name='x_{0}_{1}'.format(i,j)) for i in votants for j in centers}

    # Yj centro j es abierto
    y = { j : m.binary_var(name='y_{0}'.format(j)) for j in centers}
    
    ## RESTRICCIONES

    # TODO: TOTAL ASIGNACIONES

    # UNA SOLA ASIGNACION POR VOTANTE
    for i in votants:
        m.add_constraint(m.sum(x[i,j] for j in centers) == 1)
        
    # CUPO MAXIMO Y MINIMO
    for j in centers:
        m.add_constraint(m.sum(x[i,j] for i in votants) <= max_votants[j] * y[j]) # MAXIMO ES POR CENTRO
        m.add_constraint(m.sum(x[i,j] for i in votants) >= min_votants * y[j]) # RECORDAR QUE EL MINIMO ES IGUAL PARA TODOS LOS CENTROS


    ## FUNCIONAL TODO: IR PROBANDO

    ## OPCION 3: MINIMIZAR SUMA DE DISTANCIAS AL CUADRADO

    m.minimize(m.sum(x[i,j]*float(matrix[i-1][j-1])*float(matrix[i-1][j-1])))

    return m

# ----------------------------------------------------------------------------
# Solve the model and display the result
# ----------------------------------------------------------------------------


if __name__ == '__main__':
    distances_matrix = get_distances_matrix()
    max_votants_centers = get_max_votants_centers()
    mdl = build_diet_model(distances_matrix, max_votants_centers, 30, len(distances_matrix), len(distances_matrix[0]))
    mdl.print_information()
    if mdl.solve():
        mdl.float_precision = 3
        print("* model solved as function:")
        mdl.print_solution()
        mdl.report_kpis()
        # Save the CPLEX solution as "solution.json" program output
        with get_environment().get_output_stream("solution.json") as fp:
            mdl.solution.export(fp, "json")
    else:
        print("* model has no solution")