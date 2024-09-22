#ifndef particlePLK13D_head
#define particlePLK13D_head


#include <iostream>
#include <random>


class particlePLK13D  {
    
    public:
    
    particlePLK13D(std::mt19937* generator);
    ~particlePLK13D();
    
    void Move(double, double, double, double, std::vector<double>, std::vector<double>, std::vector<double>, double a[][3], bool, int);
    void Shuffle(double limits[][3]);
//    virtual bool Inside(double x ,double y, double z, double limits[][3]);
    bool InsideEllipse(double x ,double y, double z, double limits[][3]);
    void ChangeID(double limits[][3], std::vector<double> ratio, std::vector<double> conc0, std::vector<double> conc1, int );
//    virtual void CalcEllips(double,double);
    double funclin(double, int);
    
    double GetXpos() {return x;};
    double GetYpos() {return y;};
    double GetZpos() {return z;};
    double GetID()  {return id_particle;};
    
    void SetSettings(float, float, float, float, float, float );
    void MEXpSetSettings(float, float, float );


    private:
    
    double x;
    double y;
    double z;
    
    float k_decay;
    bool plk1_to_MEXp_slow;
    bool plk1_to_MEXp_fast;
    bool plk1_detached_when_MEXp_changes;
    
    float k_fast_slow, k_slow_fast_low, k_slow_fast_high, plk1_delay_start_time, plk1_delay_end_time ;
    
    int id_particle;

    std::mt19937* gen;
    
    
    
};

#endif
