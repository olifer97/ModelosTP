# prueba_csv.mod lee CSV de distancias

set K dimen 2;

param d{i in 1..1134, j in 1..11};

table tab_distance IN "CSV" "distancias_reducido.csv" :
  K <- [idVotante, idCentro], d ~ distancia;


printf "Number of values: %d\n", card(K);
printf {i in 1..1134, j in 1..11} : 'Votante %d recorre a centro %d %f km \n',i,j,d[i,j];
end;

