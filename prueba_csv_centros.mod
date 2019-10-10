# prueba_csv.mod lee CSV de centros

set I dimen 1;

param CupoMaxCentro{j in 1..11};

table tab_centros IN "CSV" "centros_reducido.csv" :
  I <- [id], CupoMaxCentro ~ max_votantes;


printf "Number of values: %d\n", card(I);
printf {j in 1..11} : 'Centro %d admite %d votantes\n',j,CupoMaxCentro[j];
end;
