#include <random>
#include <algorithm>
#include <map>

#include "Archivo.h"

using namespace std;


void calcular_vel(vector<Particula> &particulas, vector < vector<int> > vecinos, double min_radio, double max_radio, double dt, double beta, float tau, float L){

  float distancia;
  vector<float> enx;
  enx.resize(particulas.size(),float());
  vector<unsigned short> contactos;
  contactos.resize(particulas.size(),int());

 //aca comienza el codigo de verdad


  float dir_des_x;
  for (int i=0;i<particulas.size();i++){
     int id_vec;
     //buscar las colisiones
     for (int vec = 0; vec < vecinos[i].size(); vec++){
       id_vec = vecinos[i][vec];
       if (id_vec > i){
         distancia = abs(particulas[i].get_pos_x()-particulas[id_vec].get_pos_x());
         if (distancia - (particulas[i].get_radio()+particulas[id_vec].get_radio() ) < 0 ){
           //cout<<"Distancia:"<< distancia<< " radios: "<< particulas[i].get_radio()<<" "<<particulas[id_vec].get_radio()<<endl;
           contactos[i] += 1;
           contactos[id_vec]+=1;


           if (particulas[i].get_vel_x()*particulas[id_vec].get_vel_x() < 0){
             if (rand() < 0.5){
               particulas[i].set_invertion_true();
             }
             else{
               particulas[id_vec].set_invertion_true();
             }
           }

           enx[i] += (particulas[i].get_pos_x()-particulas[id_vec].get_pos_x())/distancia;
           enx[id_vec] += (particulas[id_vec].get_pos_x()-particulas[i].get_pos_x())/distancia;
         }
       }
     }

   }//aqui termina la primera recorrida.

   //Parte 2: asignar radios y velocidades. ()
     float nuevo_radio;
     float d;
     float modulo_v;
     float norm;
     //float nueva_velocidad[2];
     //ahora si recorro con la intencion de actualizar velocidades.
     for (int i = 0; i < particulas.size(); i++){
       dir_des_x = particulas[i].get_target_x()-particulas[i].get_pos_x();
       float d = abs(particulas[i].get_pos_x()-particulas[i].get_target_x());
       if (d==0){
         particulas[i].set_out_limit();
       }
       dir_des_x = dir_des_x/d;
       if (contactos[i] == 0 ){
           nuevo_radio = particulas[i].get_radio() + max_radio/(tau/dt);
           if (nuevo_radio > max_radio){nuevo_radio = max_radio;}
           particulas[i].set_radio(nuevo_radio);
           modulo_v = particulas[i].get_velocidad_deseada() * pow((nuevo_radio-min_radio)/(max_radio-min_radio),beta);
          particulas[i].set_vel_x(modulo_v * (dir_des_x) );
           //cout << "Velocidad de "<< particulas[i].get_id() <<" libre: modulo" << modulo_v<< endl;
       }
       else{//ha ocurrido una colision
           float vel_escape_x = particulas[i].get_velocidad_deseada()*(enx[i]);
           particulas[i].set_vel_x(vel_escape_x);
           particulas[i].set_radio(min_radio);
           if (particulas[i].was_inverted()){
             particulas[i].invert_velocidad_deseada(L,min_radio);
           }

           //cout << "Velocidad de "<< particulas[i].get_id() <<" colisonada: " << vel_escape_x << endl;
      }

    }
  }







void mover(vector<Particula> &particulas,float dt, float L, float prob, float min_radio){
  for (int i=0; i<particulas.size();i++){
    particulas[i].reset_invertion();
    particulas[i].set_pos_x(particulas[i].get_pos_x()+dt*particulas[i].get_vel_x());
    if (float(rand())/RAND_MAX < prob){
      cout<<"random inversion"<<endl;
      particulas[i].invert_velocidad_deseada(L,min_radio);
    }
    if (particulas[i].get_pos_x() < 0  || (particulas[i].get_pos_x() > L) )  {
      particulas[i].set_out_limit();
    }
    //if(isnan( particulas[i].get_pos_x() ) ){cout << "Nan encontrado, F"<<endl;}

  }
  particulas.erase(std::remove_if(particulas.begin(),
                                particulas.end(),
                                [](Particula & x){return x.is_out()==true;}),
                 particulas.end());


}



int add_particle(vector<Particula> &particulas, int higher_id,float vd, float L,float r_max){

  Particula nueva;
  //cout << "valor recibido:"<<vd<<endl;

  for (int i=0; i<particulas.size();i++){
    if (higher_id < particulas[i].get_id()){
      higher_id = particulas[i].get_id();
    }
  }
  nueva.set_id(higher_id+1);

  nueva.set_vel_x(0);

  if (rand() < RAND_MAX/2.0){
      int i = 0;
      for (i;i < particulas.size();i++){
        if (particulas[i].get_pos_x() < r_max){

          break;
        }
      }
      if (i == particulas.size()){
        nueva.set_velocidad_deseada(vd);
        nueva.set_pos_x(0);
        nueva.set_target(L);
        nueva.set_radio(r_max);
        particulas.push_back(nueva);
        higher_id+=1;
      }
  }
  else{
    int j = 0;
    for (j;j < particulas.size();j++){
      if (particulas[j].get_pos_x() > L-r_max){
        break;
      }
    }
    if (j == particulas.size()){
      nueva.set_velocidad_deseada(vd);
      nueva.set_pos_x(L);
      nueva.set_target(0);
      nueva.set_radio(r_max);
      particulas.push_back(nueva);
      higher_id+=1;
    }
  }
  //cout << "nueva: "<<nueva.get_id()<<" " << nueva.get_velocidad_deseada()<<endl;

return (higher_id);
}
















map<float,float> get_inverted_cdf(vector<float> dist_original){

  map<float,float> inverted_cdf;

  //Crear CDF
  int n = dist_original.size();
  sort(dist_original.begin(),dist_original.end());

  for (int i=0;i<n;i++){
    inverted_cdf.insert( pair<float,float>(float(i)/n,dist_original[i]) );

  }
  return (inverted_cdf);
}


float valor_segun_inverted_cdf(float uniform, map<float,float> inverted_cdf){

  float new_val;
  float low = inverted_cdf.lower_bound(uniform)->first;
  float high = inverted_cdf.upper_bound(uniform)->first;
  new_val = (inverted_cdf[low] + inverted_cdf[high])/2.0;
  return new_val;


}
