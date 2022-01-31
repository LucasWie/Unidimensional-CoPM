#include <vector>
//#include <ctime>
#include <string>
#include <fstream>
#include <algorithm>
#include <random>
#include <time.h>

using namespace std;

vector <Particula> ubicar_particulas(int N,float L,float min_dist,vector<float> v_des){
  //srand(time(NULL));



  double distancia;
  int i = 0;
  int j;
  vector <Particula> particulas;
  Particula aux;

  //int N = 200;
  while (i < N){
      float nuevo_x = (rand()/float(RAND_MAX))*L;
      //cout << i << endl;

    for (j=0; j<i; j++){//ver si no se superpone con otra particula ya puesta.
      distancia = abs(particulas[j].get_pos_x() - nuevo_x);
      if (distancia < min_dist){//hay superposicion, buscar nueva posicion
        break;
      }
    }
    if (j == i){ //si recorrí todas las particulas previamente ubicadas sin colisiones, paso a la siguente
      //cout<<"i vale: " <<i<<endl;
      aux.set_id(i);
      aux.set_pos_x(nuevo_x);
      aux.set_vel_x(0);
      aux.set_velocidad_deseada(v_des[i]);
      cout << "Pa particula " << i <<" tiene vd: "<<v_des[i] <<endl;
      aux.set_radio(min_dist/2.0);
      if (rand() < RAND_MAX/2.0){
        aux.set_target(L);
      }
      else{
        aux.set_target(0);
      }
      particulas.push_back(aux);
      i++;
      }
  }

  return particulas;
}
