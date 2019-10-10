/* Declaración de constantes*/

param N; /*cant votantes*/
param C; /*cant centros*/

param CupoMinCentro; /*el mismo para todos los centros*/

set I dimen 1;
param CupoMaxCentro{j in 1..C};

set K dimen 2;
param D{i in 1..N, j in 1..C}; /*distancia del votante i al centro j*/

table tab_centros IN "CSV" "centros_reducido.csv" :
I <- [id], CupoMaxCentro ~ max_votantes;

table tab_distance IN "CSV" "distancias_reducido.csv" :
K <- [idVotante, idCentro], D ~ distancia;

/* Declaración de variables*/
var X{i in 1..N,j in 1..C} binary; /*asignacion del votante i al centro j*/
var Y{j in 1..C} binary;           /*el centro j es habilitado*/

/* Definición del funcional */

#Minimizar el promedio de las distancias al cuadrado
minimize z: (sum {i in 1..N, j in 1..C} X[i,j]*D[i,j]*D[i,j])/N;

#Minimizar el promedio de las distancias
#minimize z: (sum {i in 1..N, j in 1..C} X[i,j]*D[i,j])/N;

/* Restricciones */

s.t. ASIGNACION_UNICA{i in 1..N}: 1 = sum {j in 1..C} X[i,j];
s.t. TOTAL_ASIGNACIONES: sum {i in 1..N, j in 1..C} X[i,j]=N;
s.t. CAPAC_TOTAL_CENTROS: sum {j in 1..C} CupoMaxCentro[j] * C >=N;
s.t. CUPOMAX_CENTRO{j in 1..C}: sum {i in 1..N} X[i,j]<= Y[j] * CupoMaxCentro[j];
s.t. CUPOMIN_CENTRO{j in 1..C}: Y[j] * CupoMinCentro <= sum {i in 1..N} X[i,j];


solve;

printf {i in 1..N, j in 1..C: X[i,j]>=1} : 'Votante %f recorre a centro %f %f km \n',i,j,D[i,j];

end;
