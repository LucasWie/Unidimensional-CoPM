#include <iostream>
#include <fstream>
#include <list>
#include <vector>
#include <string>

//#include "Particula.h"
using namespace std;





void set_cantidad(string nombre_salida, int n,float pasos){
  ofstream salida (nombre_salida);
  //cout << pasos <<endl;
  //salida << n <<"," << pasos << endl;
  salida.close();

}


vector<float> cargar_dist(string filename){
  ifstream archi;
  cout << filename <<endl;
  archi.open(filename.c_str());
  if (archi.is_open()){
    cout << "si abrio el archivo"<<endl;
  }
  else{
    cout << "NO se abriò el archivo"<<endl;
  }
  vector<float> values;
  float v;
  while(archi >> v){
    //cout << v<<endl;
    values.push_back(v);

  }

  return(values);
}


void  escribir_posiciones(string nombre_salida, vector<Particula> particulas,float tiempo_acumulado, int canal){
  //string ruta = "/home/lucas/Escritorio/Doctorado/Curso_simulacion//";
  nombre_salida = nombre_salida;//ruta + ...
  ofstream salida (nombre_salida,ios::app);

  int N = particulas.size();
  //salida << tiempo_acumulado << endl;
  for (int i=0; i<N; i++){
    salida << particulas[i].get_id() << ",";
    salida << particulas[i].get_pos_x() << ",";

//    salida << particulas[i].get_pos_y() << ",";
    salida << particulas[i].get_vel_x()<< ",";

    salida << tiempo_acumulado <<",";
    //salida << "Pikachu yo te elijo" <<" ,";

    salida << canal<<",";
    salida << particulas[i].get_radio();

  //  salida << particulas[i].get_vel_y() << ",";
    salida << "\n";

  }
  salida.close();
}
