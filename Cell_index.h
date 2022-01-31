#include <iostream>
#include <math.h>
#include <list>
#include <cstdlib>
#include <ctime>
#include <string>
#include <vector>


using namespace std;


vector<vector<int> > calcular_vecinos(vector<Particula> &particulas, float r_max, float L){
//inicializacíon
    float minima_distancia = 0;
    vector<vector<int> > vecinos;

    int N = particulas.size();
    vecinos.resize(N);
    for(int i=0; i<N; i++){

      //Condisciones de borde cuando casi 0
      if (particulas[i].get_pos_x() < r_max){
        for(int j = i+1; j < N; j++){
          if (abs(particulas[i].get_pos_x()+L-particulas[j].get_pos_x()) < r_max){
            vecinos[i].push_back(j);
            vecinos[j].push_back(i);
          }
        }
      }

      if (particulas[i].get_pos_x() > L-(r_max) ){
        for(int j = i+1; j < N; j++){
          if (abs(particulas[i].get_pos_x()-L-particulas[j].get_pos_x()) < r_max){
            vecinos[i].push_back(j);
            vecinos[j].push_back(i);
          }
        }
      }




      for(int j=i+1; j<N; j++){
        if (abs(particulas[i].get_pos_x()-particulas[j].get_pos_x()) < r_max){
          //cout << "vecinos:" <<i <<" and " <<j <<endl;
          vecinos[i].push_back(j);
          vecinos[j].push_back(i);
        }
        // Parte de manejo de limites (Lo hice periodico solo en x)



      }
    }

return vecinos;

}
