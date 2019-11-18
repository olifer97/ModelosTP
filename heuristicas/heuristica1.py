#!/usr/bin/env python3
import random
import csv

#CONSTANTES DEL REDUCIDO
N = 1134
C = 30
MIN_CUPO = 30

def ordenar_distancias(dists):
    return sorted(dists,key=lambda x: x[1])

def centros_cupos_minimos_completos(centros):
    for centro in centros.keys():
        if len(centros[centro]) > 0 and len(centros[centro]) < MIN_CUPO:
            return False
    return True

def heuristica(dists, cupos):
    center_votant = {}
    votants = []
    for i in range(1,C+1):
        center_votant[i] = []
    for i in range(1,N+1):
        votants.append(i)
    
    #asignacion inicial
    while len(votants):
        for votant in votants:
            order_dists = ordenar_distancias(dists[votant])
            for center,dist in order_dists:
                if len(center_votant[center]) < cupos[center]:
                    center_votant[center].append(votant)
                    votants.remove(votant)
                    break

    #cumplimiento de cupo minimo
    while not centros_cupos_minimos_completos(center_votant):
        # una opcion es agarrar los centros que menos votantes tienen primero, o random
        #for centro in sorted(center_votant.keys(), key=lambda x: len(center_votant[x])):
        centro = random.randint(1,C)
        if len(center_votant[centro]) > 0 and len(center_votant[centro]) < MIN_CUPO:
            #vaciarlo
            votantes = center_votant[centro]
            while len(votantes): #los reasigno
                for votant in votantes:
                    order_dists = ordenar_distancias(dists[votant])
                    for center,dist in order_dists:
                        if len(center_votant[center]) < cupos[center] and len(center_votant[center]) > 0  and center != centro:
                            center_votant[center].append(votant)
                            votantes.remove(votant)
                            break
    return center_votant


def main():
    distancias = {}
    distancias2 = {}
    distancias_totales= []
    cupos = {}
    with open('../datos/distancias_reducido.csv', 'r') as dists:
        distsCSV = csv.reader(dists, delimiter=',')
        next(distsCSV, None)
        for votant in distsCSV:
            distancias[int(votant[0])] = distancias.get(int(votant[0]), [])
            distancias[int(votant[0])].append((int(votant[1]), float(votant[2])))

            distancias2[(int(votant[0]), int(votant[1]))] = distancias.get((int(votant[0]), int(votant[1])), 0) 
            distancias2[(int(votant[0]), int(votant[1]))] += float(votant[2])

            distancias_totales.append(float(votant[2]))
    
    print(sum(distancias_totales) / len(distancias_totales) )
    print(max(distancias_totales))

    with open('../datos/centros_reducido.csv', 'r') as centers:
        centersCSV = csv.reader(centers, delimiter=',')
        next(centersCSV, None)
        for center in centersCSV:
            cupos[int(center[0])] = int(center[3])

    asignaciones = heuristica(distancias, cupos)
    distancias3 = []
    for centro in asignaciones.keys():
        votantes = asignaciones[centro]
        print("Centro {} tiene {} votantes asignados".format(centro, len(votantes)))
        for votante in votantes:
            distancias3.append(distancias2[(votante,centro)])
    
    print(sum(distancias3) / len(distancias3) )
    print(max(distancias3))
    
    
if __name__ == "__main__":
    main()