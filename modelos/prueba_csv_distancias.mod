# prueba_csv.mod lee CSV de distancias

set K dimen 2;

param d{i in 1..1134, j in 1..11};

table tab_distance IN "CSV" "../datos/distancias_reducido.csv" :
  K <- [idVotante, idCentro], d ~ distancia;

printf "Cantidad de distancias en csv: %d\n", card({i in 1..1134, j in 1..11: d[i,j]});
printf "Maxima distancia: %f\n", max{i in 1..1134, j in 1..11} d[i,j];
printf "Minima distancia: %f\n", min{i in 1..1134, j in 1..11} d[i,j];
printf "Distancia promedio: %f\n", (sum{i in 1..1134, j in 1..11} d[i,j]) /  card({i in 1..1134, j in 1..11: d[i,j]});

#printf {i in 1..1134, j in 1..11} : 'Votante %d recorre a centro %d %f km \n',i,j,d[i,j];
end;

