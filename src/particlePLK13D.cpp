#include <particlePLK13D.h>
#include <iostream>
#include <random>
#include <math.h>       /* pow */
#include <fstream>

particlePLK13D::particlePLK13D(std::mt19937* generator):x(0)
,y(0),z(0),id_particle(0)
{
// 0 unbound
// 1 bound to slow
// 2 bound to fast
    gen = generator;
    
    
}

void particlePLK13D::SetSettings(float k_to_slow_, float k_to_fast_, float k_decay_, float plk1_detached_when_MEXp_changes_, float plk1_delay_start_time_, float plk1_delay_end_time_){
    
    
    plk1_to_MEXp_slow = k_to_slow_;
    plk1_to_MEXp_fast = k_to_fast_;
    k_decay = k_decay_;
    plk1_detached_when_MEXp_changes = plk1_detached_when_MEXp_changes_;
    plk1_delay_start_time = plk1_delay_start_time_;
    plk1_delay_end_time = plk1_delay_end_time_;
    
}

void particlePLK13D::MEXpSetSettings(float k_fast_slow_, float k_slow_fast_low_, float k_slow_fast_high_){
    
    
    k_fast_slow = k_fast_slow_;
    k_slow_fast_low = k_slow_fast_low_;
    k_slow_fast_high = k_slow_fast_high_;
    
    
}


particlePLK13D::~particlePLK13D()
{
    
}

void particlePLK13D::Shuffle(double limits[][3]){
    


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

bool particlePLK13D::InsideEllipse(double x_ ,double y_, double z_, double limits[][3]){

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

void particlePLK13D::ChangeID(double limits[][3], std::vector<double> ratio, std::vector<double> conc0, std::vector<double> conc1, int time){
    

    if (id_particle==2 || id_particle==1){
        
        
        std::uniform_real_distribution<> dist(0,1);
        double val = dist(*gen);

        if (val<k_decay)
        id_particle=0;
        else {
            //Second nightmare
            
            if (id_particle ==1 ){
                std::uniform_real_distribution<> dist(0,1);
                double val = dist(*gen);
                
                if (val<funclin(x, time)){
                    if (!plk1_detached_when_MEXp_changes)
                        id_particle = 2;
                    else
                        id_particle = 0;

                }
            }
            
            else if (id_particle ==2){
                std::uniform_real_distribution<> dist(0,1);
                double val = dist(*gen);
                if (val < k_fast_slow){
                    if (!plk1_detached_when_MEXp_changes)
                        id_particle = 1;
                    else
                        id_particle = 0;
            
                }
                
            }

        
        }
 
    }
    else {

        
        
        if (bool(plk1_to_MEXp_slow) && !bool(plk1_to_MEXp_fast)){
            
            //PLK1 goes only to MEXp SLOW!
            
            //calcolate k rate
            
            double k_rate = conc0[int(x)];

            std::uniform_real_distribution<> dist(0,1);
            double val = dist(*gen);
            
            if (val<k_rate){
                
                id_particle=1;
            }
            
            
            
        }
        
        else if (!bool(plk1_to_MEXp_slow) && bool(plk1_to_MEXp_fast)){
            
            //PLK1 goes only to MEXp FAST!
            
            //calcolate k rate
            
            double k_rate = conc1[int(x)];
            std::uniform_real_distribution<> dist(0,1);
            double val = dist(*gen);
            
            if (val<k_rate){
                
                id_particle=2;
            }
        
        }
        
        else if(bool(plk1_to_MEXp_slow) && bool(plk1_to_MEXp_fast)) {
         
            double k_rate = conc1[int(x)]+conc0[int(x)];
            std::uniform_real_distribution<> dist(0,1);
            double val = dist(*gen);
            
            if (val<k_rate){
             
                double ratio_con = ratio[int(x)];
             
                std::uniform_real_distribution<> dist(0,1);
                double val = dist(*gen);
             
                if (val<ratio_con/(ratio_con+1)){
                    id_particle=1;
             
                }
                else {
                    id_particle=2;
                }
             
            }
            
        
        }
        
        
        
        
        
    }

    
}

double particlePLK13D::funclin(double x_, int t){


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

void particlePLK13D::Move(double v0, double v1, double v2, double dt, std::vector<double> ratio, std::vector<double> conc0, std::vector<double> conc1, double limits[][3], bool nobound, int time ){
    
    double v = 0;
    
    
    if (id_particle ==0 ){
        v = v0;
    }
    
    else if (id_particle ==1){
        v=v1;
    }
    
    else if (id_particle ==2){
        v=v2;
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
    
// between 350 and 500 linearly increases
		
		double val_mbk2 = 0.0;
		if (time<plk1_delay_start_time){
			
		}
		else if(time>plk1_delay_end_time){
			val_mbk2 = 1.0;
		}
		else {
			val_mbk2 = ((double)(1.0-0.0)/(plk1_delay_end_time-plk1_delay_start_time))*(time-plk1_delay_start_time);
		}
		std::uniform_real_distribution<> dist(0, 1);
        double val_prob = dist(*gen);
		
        
		
 		if (id_particle == 0 && val_prob <= val_mbk2){
			
			ChangeID(limits, ratio, conc0, conc1, time);
		}
        else if (id_particle!=0){
            ChangeID(limits, ratio, conc0, conc1, time);

        }
}

