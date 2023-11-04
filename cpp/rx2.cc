#include <iostream>
#include <iomanip>
#include <pigpio.h>
#include <chrono>
#include <unistd.h>

void callback(int gpio, int level, uint32_t tick) {

    
    std::cout << tick<<" "<<level<<std::endl;

}

int main(int argc, char** argv) {

    int pin = 11;

    if (gpioInitialise()<0) return 1;
    gpioSetMode(pin, PI_INPUT);

    gpioSetAlertFunc(pin, callback);

    while(true) {
        sleep(1);
    }
    

    gpioTerminate();
}