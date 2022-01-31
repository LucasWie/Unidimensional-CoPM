#include <iostream>
#include <list>
#include <math.h>
#include <vector>

using namespace std;

class Particula{
  private:
    int id;
    double pos_x = 0;
    double vel_x = 0;

    double radio = 0;
    double masa = 0;

    double target_x = 0;
    bool out_of_l = false;

    int target = 0;
    int origen = 0;
    bool inverted_flag = false;

    double velocidad_deseada = 0;

  public:
    Particula(){
      int id;
      double pos_x = 0;
      double vel_x = 0;
      double radio = 0;
      //double masa = 0;

      double target_x = 0;
      bool out_of_l = false;
      double velocidad_deseada = 0;
      bool inverted_flag = false;
    }
    Particula(const Particula& a_copiar);

    bool operator==(const Particula& a_comparar)const ;
    void set_out_limit(){
      this->out_of_l = true;
    }
    void set_id(int nuevo_id){id = nuevo_id;}
    void set_radio(double r){radio = r;}
    void set_velocidad_deseada(double v){velocidad_deseada = v;}
    void set_pos_x(double x) {pos_x = x;}
    void set_vel_x(double v) {vel_x = v;}
    void set_target(double x){
      //cout << "Se setearon los target: "<< x <<" "<< y <<endl;
      target_x = x;
    }

    double get_pos_x()const {return pos_x;}
    double get_vel_x()const {return vel_x;}
    double get_velocidad_deseada()const {return velocidad_deseada;}
    double get_radio()const {return radio;}
    double get_target_x()const {return target_x;}




    bool is_out() {return out_of_l;}

    void invert_velocidad_deseada(float L, float min_radio){
      if (this->get_target_x()==L){
        this->set_target(0);
      }
      else{
        this->set_target(L);
      }
      this->set_radio(min_radio);
    }
    bool was_inverted(){return inverted_flag;}
    void set_invertion_true(){inverted_flag = true;}
    void reset_invertion(){inverted_flag = false; }
    int get_id()const {return id;}

    };

bool is_out_of_limit(Particula p){return p.is_out();}


Particula::Particula (const Particula& a_copiar){
  id = a_copiar.id;
  pos_x = a_copiar.pos_x;
  vel_x = a_copiar.vel_x;
  radio = a_copiar.radio;
  masa = a_copiar.masa;
  target_x = a_copiar.target_x;
  velocidad_deseada = a_copiar.velocidad_deseada;

}
bool Particula::operator==(const Particula& a_comparar) const{
  if(this->id == a_comparar.id)
   return(1);
  else{return(0);}
}
