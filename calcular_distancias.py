#!/usr/bin/env python3
from math import radians, cos, sin, asin, sqrt
import csv

def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8 # this is in miles.  For Earth radius in kilometers use 6372.8 km

    dLat = lat2 - lat1
    dLon = lon2 - lon1
    lat1 = lat1
    lat2 = lat2

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c


  

## MATRIZ CON DISTANCIAS[i,j] i es el votante j el centro
def main():
    with open('distancias_matrix.csv', 'w') as dists:
        distsCSV = csv.writer(dists, delimiter=',')
        with open('votantes_reducido.csv') as votants:
            votantsCSV = csv.reader(votants, delimiter=',')
            next(votantsCSV, None)
            for votant in votantsCSV:
                dists_votant = []
                with open('centros_reducido.csv') as centers:
                    centersCSV = csv.reader(centers, delimiter=',')
                    next(centersCSV, None)
                    for center in centersCSV:
                        if len(center) == 0: break
                        distance = haversine(float(votant[1]),float(votant[2]),float(center[1]),float(center[2]))
                        dists_votant.append(distance)

                distsCSV.writerow(dists_votant)

if __name__ == "__main__":
    main()