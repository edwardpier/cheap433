fn main() {
    use rppal::gpio::Gpio;
    use rppal::gpio::Trigger;

    const PIN: u8 = 11;


    let gpio = match Gpio::new() {
        Ok(gpio) => gpio,
        Err(_) => {
            panic!("Could not create gpio interface");
        }
    };

    let pin = match gpio.get(PIN) {
        Ok(pin) => pin,
        Err(_) => {
            panic!("could not get pin");
        }
    };
    
    let mut pin = pin.into_input();
    match pin.set_interrupt(Trigger::Both) {
        Ok(()) => (),
        Err(_) => {
            panic!("Error setting interrupt");
        }
    };

    let opt = match pin.poll_interrupt(false, None) {
        Ok(opt) => opt,
        Err(_) => {
            panic!("Error polling for interrupt")
        }
    };


    println!("{}", opt);
}
