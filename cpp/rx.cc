#include <iostream>
#include <iomanip>
#include <pigpio.h>
#include <chrono>

int main(int argc, char** argv) {

    int pin = 11;

    if (gpioInitialise()<0) return 1;
    gpioSetMode(pin, PI_INPUT);

   
    int was = gpioRead(pin);
    std::chrono::steady_clock::time_point time0 = std::chrono::steady_clock::now();
    std::cout << 0.000000000<<" "<<was<<std::endl;
    while(true) {


        
        
        int on = gpioRead(pin);
        std::chrono::steady_clock::time_point now = std::chrono::steady_clock::now();

        if(on != was) {
            std::chrono::nanoseconds time_span = std::chrono::duration_cast<std::chrono::nanoseconds>(now - time0);
            double sec = time_span.count()/1e9;
            std::cout <<std::fixed<<std::setprecision(9)<<sec<<" "<<was<<std::endl;
            std::cout <<std::fixed<<std::setprecision(9)<<sec<<" "<<on<<std::endl;
            was = on;

        }
    }

        
    


    gpioTerminate();


}