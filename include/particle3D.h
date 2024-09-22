#ifndef particle_3D
#define particle_3D


#include <iostream>
#include <random>


class particle3D  {
    
    public:
    
    particle3D(std::mt19937* generator);
    ~particle3D();
    
    void Move(double, double, double, double a[][3], bool, double);
    void Shuffle(double limits[][3]);
//    virtual bool Inside(double x ,double y, double z, double limits[][3]);
    bool InsideEllipse(double x ,double y, double z, double limits[][3]);
    void ChangeID(double limits[][3], double);
//    virtual void CalcEllips(double,double);
    double funclin(double, double);
    
    double GetXpos() {return x;};
    double GetYpos() {return y;};
    double GetZpos() {return z;};
    double GetID()  {return id_particle;};
    
    void SetSettings(float, float, float, float, float );


    private:
    
    double x;
    double y;
    double z;
    
    float initial_slow, initial_fast, k_fast_slow, k_slow_fast_low, k_slow_fast_high;
    
    int id_particle;

    std::mt19937* gen;
    
    
    
};

#endif
