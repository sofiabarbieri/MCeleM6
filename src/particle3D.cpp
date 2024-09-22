#include <particle3D.h>
#include <iostream>
#include <random>
#include <math.h>       /* pow */
#include <fstream>

particle3D::particle3D(std::mt19937* generator ):x(0)
,y(0),z(0),id_particle(-1)
{
    gen = generator;
    
}

void particle3D::SetSettings(float initial_slow_, float initial_fast_, float k_fast_slow_, float k_slow_fast_low_, float k_slow_fast_high_){
    
    
    initial_slow = initial_slow_;
    initial_fast = initial_fast_;
    k_fast_slow = k_fast_slow_;
    k_slow_fast_low = k_slow_fast_low_;
    k_slow_fast_high = k_slow_fast_high_;
    
}
particle3D::~particle3D()
{
    
}

void particle3D::Shuffle(double limits[][3]){
    
    std::uniform_real_distribution<> dist;
    double val = dist(*gen);
    
    if (val<initial_slow)
        id_particle = 0;
    else
        id_particle = 1;
    
    auto center_x = (limits[1][0]-limits[0][0])/2;
    auto center_y = (limits[1][1]-limits[0][1])/2;
    auto center_z = (limits[1][2]-limits[0][2])/2;
    
    auto semi_x = center_x;
    auto semi_y = center_y;
    auto semi_z = center_z;
    
    double x_ =0;
    double y_ =0;
    double z_ =0;
    
    double sign = 2;
    
    while(sign > 1){
        
        {
        std::uniform_real_distribution<> dist(limits[0][0], limits[1][0]);
        x_ = dist(*gen);
        };
        {
        std::uniform_real_distribution<> dist(limits[0][1], limits[1][1]);
        y_ = dist(*gen);
        };
        {
        std::uniform_real_distribution<> dist(limits[0][2], limits[1][2]);
        z_ = dist(*gen);
        };
        
        sign = pow(x_-center_x,2)/pow(semi_x,2)+pow(y_-center_y,2)/pow(semi_y,2)+pow((z_-center_z),2)/pow(semi_z,2);
    }
    x = x_;
    y = y_;
    z = z_;
    
}

bool particle3D::InsideEllipse(double x_ ,double y_, double z_, double limits[][3]){
    
//    if (x_>limits[0][0] && x_<limits[1][0] && y_>limits[0][1] && y_<limits[1][1] &&  z_>limits[0][2] && z_<limits[1][2])
//    return true;
//    else
//    return false;

    auto center_x = (limits[1][0]-limits[0][0])/2;
    auto center_y = (limits[1][1]-limits[0][1])/2;
    auto center_z = (limits[1][2]-limits[0][2])/2;
    
    auto semi_x = center_x;
    auto semi_y = center_y;
    auto semi_z = center_z;
    
    double sign = pow((x_-center_x),2)/pow(semi_x,2)+pow((y_-center_y),2)/pow(semi_y,2)+pow((z_-center_z),2)/pow(semi_z,2);
    
    if (sign<=1.)
    return true;
    else
    return false;
    
    
}

void particle3D::ChangeID(double limits[][3], double t){
    
    if (id_particle ==0 ){
        std::uniform_real_distribution<> dist(0,1);
        double val = dist(*gen);
    
        if (val<funclin(x, t))
        id_particle = 1;
    }
    
    else if (id_particle ==1){
        std::uniform_real_distribution<> dist(0,1);
        double val = dist(*gen);
        if (val < k_fast_slow)
        id_particle = 0;
    }
    
}

double particle3D::funclin(double x_, double t){
    
    if (t<300){
        double m_pendenza = (((k_slow_fast_high-k_slow_fast_low)/50)-0)/300;
    
        double m_actual = m_pendenza*t;

        return m_actual*x_+k_slow_fast_low;



    }
    else {
        double m = (k_slow_fast_high-k_slow_fast_low)/50;
        return m*x_+k_slow_fast_low;
    }
}

void particle3D::Move(double v0, double v1, double dt, double limits[][3], bool nobound, double t){
    
    double v = 0;
    
    
    if (id_particle ==0 ){
        v = v0;
    }
    
    else if (id_particle ==1){
        v=v1;
    }
    
    double theta=0;
    double phi = 0;
    
    {
        std::uniform_real_distribution<> dist(0, 2*M_PI);
        theta = dist(*gen);
    };
    
    {
        std::uniform_real_distribution<> dist(0, M_PI);
        phi = dist(*gen);
    };
    
    auto x_ = (x + v*cos(theta)*sin(phi)*dt);
    auto y_ = (y + v*sin(theta)*sin(phi)*dt);
    auto z_ = (z + v*cos(phi)*dt);
    
    if(nobound){
        
        double t_rem = dt;
        double dt_ = dt;

        if (InsideEllipse(x_, y_, z_, limits)==false){
            
            while(InsideEllipse(x_, y_, z_, limits)==false){
            
                dt_ = dt_/1.01;
                
                x_ = (x + v*cos(theta)*sin(phi)*dt_);
                y_ = (y + v*sin(theta)*sin(phi)*dt_);
                z_ = (z + v*cos(phi)*dt_);
            
            }
            
            x = x_;
            y = y_;
            z = z_;
            
            {
                std::uniform_real_distribution<> dist(0, 2*M_PI);
                theta = dist(*gen);
            };
            
            {
                std::uniform_real_distribution<> dist(0, M_PI);
                phi = dist(*gen);
            };
            
            t_rem = dt-dt_;
            
            x_ = (x + v*cos(theta)*sin(phi)*t_rem);
            y_ = (y + v*sin(theta)*sin(phi)*t_rem);
            z_ = (z + v*cos(phi)*t_rem);
            
            while(InsideEllipse(x_, y_, z_, limits)==false){
            
                {
                    std::uniform_real_distribution<> dist(0, 2*M_PI);
                    theta = dist(*gen);
                };
                
                {
                    std::uniform_real_distribution<> dist(0, M_PI);
                    phi = dist(*gen);
                };
                
                
                x_ = (x + v*cos(theta)*sin(phi)*t_rem);
                y_ = (y + v*sin(theta)*sin(phi)*t_rem);
                z_ = (z + v*cos(phi)*t_rem);
                
            }
            
            x = x_;
            y = y_;
            z = z_;
        
        }
        else {
            x = x_;
            y = y_;
            z = z_;
        }
  
    }
    else{
        while(InsideEllipse(x_, y_, z_, limits)==false){
            
            {
                std::uniform_real_distribution<> dist(0, 2*M_PI);
                theta = dist(*gen);
            };
            
            {
                std::uniform_real_distribution<> dist(0, M_PI);
                phi = dist(*gen);
            };
            
            x_ = (x + v*cos(theta)*sin(phi)*dt);
            y_ = (y + v*sin(theta)*sin(phi)*dt);
            z_ = (z + v*cos(phi)*dt);
            
            
        }
        
        x = x_;
        y = y_;
        z = z_;
        
    }
    
    ChangeID(limits, t);
}

