#include <vector>
#include <string>
#include <cmath>
#include <ctime>
#include <stdlib.h>
#include <unistd.h>
#include <map>


#include "Particula.h"
#include "funciones2.h"
#include "set_particulas.h"
#include "Cell_index.h"


using namespace std;

int main(){
  vector<Particula> particulas;
  //double velocidad_deseada = 5.0;
  double r_min = 12.0/2;
  double r_max = 30/2.0;
  float beta = 0.9;
  float tau = 3;
  //float inversion_prob_min = 3.0/1900;
  float inversion_prob_min = 3.0/1900;
  float prob_inversion_step;



  vector <float> r_mins = {3,5,7,9,11};
  vector <string> r_mins_names = {"3","5","7","9","11"};

  vector <float> r_maxs = {12,15,18,21,24};
  vector <string> r_max_names = {"12","15","18","21","24"};




  srand(144);

  int N_max = 6;
  int n_ini = 4;
  float L = 700;
  float t_max =  360;
  string ruta = "./parameter_evaluation/" ;
  string comando = "mkdir -p "+ruta;
  system(comando.c_str());
  string nombre_salida;
  string nombre_salida_base;

  vector<float> vd_iniciales;


  vector<float> velocidades_reales;

  velocidades_reales = cargar_dist("velocidades_aisaldas.txt");

  //cout <<velocidades_reales.size()<<endl;

  float vel_max_esperada = *max_element(velocidades_reales.begin(),velocidades_reales.end());

  map<float,float> inv_cdf = get_inverted_cdf(velocidades_reales);
  float uniform_dist_pick;



  for (int test_rmin = 0; test_rmin < 5; test_rmin++){
      r_min = r_mins[test_rmin];

      for (int test_rmax = 0; test_rmax < 5; test_rmax++){
        r_max = r_maxs[test_rmax];



      float dt = (r_min / (2*vel_max_esperada) );
      prob_inversion_step = inversion_prob_min*dt;
      vector<vector<int> > vecinos;



      nombre_salida_base = ruta +"/t_cells_";
      nombre_salida = nombre_salida_base+"rmin_"+r_mins_names[test_rmin]+"rmin_"+r_max_names[test_rmax]+".txt";
      //nombre_salida = nombre_salida_base+".txt";
      set_cantidad(nombre_salida, n_ini,t_max/dt);
      int last_id;
      for (int canal = 0; canal < 20; canal++ ){
        vd_iniciales.clear();
        for (int part_ini=0;part_ini<n_ini;part_ini++){
              uniform_dist_pick = float(rand())/RAND_MAX;
              vd_iniciales.push_back(valor_segun_inverted_cdf(uniform_dist_pick, inv_cdf));
        }
          particulas = ubicar_particulas(n_ini,L, r_min*2,vd_iniciales);//tengo las particulas en sus posiciones iniciales
          float t = 0;
          last_id = n_ini-1;
          //escribir_posiciones(nombre_salida_base +".txt",particulas,0);

          escribir_posiciones(nombre_salida,particulas,0,canal);
          for (int i = 1; i<(t_max/dt); i++){//for del tiempo
            t = t + dt;
            //cout << "Tiempo: " << t << endl;
            vecinos = calcular_vecinos(particulas,r_max*2,L);
            calcular_vel(particulas, vecinos, r_min, r_max, dt, beta,tau,L);
            mover(particulas, dt, L, prob_inversion_step,r_min);


            if(t >= round(t)  && (t - round(t) < dt)){
              escribir_posiciones(nombre_salida,particulas,(t),canal);
              if (float(rand())/RAND_MAX < float((N_max-particulas.size()))/N_max) {
                uniform_dist_pick = float(rand())/RAND_MAX;
                float vd = valor_segun_inverted_cdf(uniform_dist_pick, inv_cdf);
                //cout << vd << endl;
                last_id = add_particle(particulas,last_id,vd, L,r_max);
              }
            }
          }

        }
        cout<<"Fin del sistema "<<endl;
    }
  }



return(0);
}
