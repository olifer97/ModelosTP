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
var L{i in 1..N} >= 0;             /*km que recorre el votante i*/
var Lmax >= 0;                     /*kilometros recorridos maximos*/

/* Definición del funcional */

#Minimizar el promedio de las distancias al cuadrado
#minimize z: (sum {i in 1..N, j in 1..C} X[i,j]*D[i,j]*D[i,j])/N;

#Minimizar el promedio de las distancias
#minimize z: (sum {i in 1..N, j in 1..C} X[i,j]*D[i,j])/N;

#Minimizar el total de las distancias
#minimize z: sum {i in 1..N, j in 1..C} X[i,j]*D[i,j];

#Minimizar maxima distancia recorrida
#minimize z: Lmax;

#Minimizar la suma del maximo con el promedio
minimize z: Lmax + (sum {i in 1..N, j in 1..C} X[i,j]*D[i,j])/N;

/* Restricciones */

s.t. ASIGNACION_UNICA{i in 1..N}: 1 = sum {j in 1..C} X[i,j];
s.t. TOTAL_ASIGNACIONES: sum {i in 1..N, j in 1..C} X[i,j]=N;
#s.t. CAPAC_TOTAL_CENTROS: sum {j in 1..C} CupoMaxCentro[j] * C >=N;
s.t. CUPOMAX_CENTRO{j in 1..C}: sum {i in 1..N} X[i,j]<= Y[j] * CupoMaxCentro[j];
s.t. CUPOMIN_CENTRO{j in 1..C}: Y[j] * CupoMinCentro <= sum {i in 1..N} X[i,j];

s.t. DISTANCIA_RECORRIDA{i in 1..N}: L[i] = sum {j in 1..C} X[i,j] * D[i,j];
s.t. DISTANCIA_MAXIMA{i in 1..N}: Lmax >= L[i];


solve;

printf {i in 1..N, j in 1..C: X[i,j]>=1} : 'Votante %d recorre a centro %d %f km \n',i,j,D[i,j];
printf "La maxima distancia que recorre un votante es: %f\n", max{i in 1..N, j in 1..C:X[i,j]>=1} D[i,j]*X[i,j];
printf "La minima distancia que recorre un votante es: %f\n", min{i in 1..N, j in 1..C:X[i,j]>=1} D[i,j]*X[i,j];
printf "La distancia promedio es: %f\n", (sum{i in 1..N, j in 1..C:X[i,j]>=1} D[i,j]*X[i,j]) / N;

/*escribo el resultado en un csv*/
table tab_result{(i,j) in K:X[i,j]>=1} OUT "CSV" "result2.csv" :
  i ~ idV, j ~ idC, X[i,j] ~asignado, D[i,j] ~distancia;

end;
