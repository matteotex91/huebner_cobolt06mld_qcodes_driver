from typing import Any
import pyvisa


class HuebnerCobolt06mld:
    """
    Initialize a new Huebner Cobolt 06 mld laser driver.
    The wavelength, maximum power and maximum current have to be specified since it is not possible to retrieve them from the serial number.

    """

    def __init__(
        self,
        name: str,
        address: str,
        max_power: float,
        max_current: float,
        wavelength: float,
    ) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the laser
        address : str
            The physical address of the laser (example: ASLR3)
        max_power : float
            The maximum power of this model, expressed in Watts
        max_current : float
            The maximum current of this model, espressed in Amperes
        wavelength : float
            The wavelength of this model, espressed in nm. This value is saved in the object as a reminder, it's not used by the driver.
        """

        self.name = name
        self.address = address
        self.wavelength = wavelength
        self.max_power = max_power
        self.max_current = max_current

        rm = pyvisa.ResourceManager()
        self.instrument = rm.open_resource(
            resource_name=address, read_termination="\r\n"
        )

    def get_status(self) -> int:
        return int(self.instrument.query("l?"))

    def set_status(self, status: int) -> None:
        if status == 1 or status == 0:
            self.instrument.write(f"l{status}")

    def get_analog_modulation_state(self) -> int:
        return int(self.instrument.query("games?"))

    def set_analog_modulation_state(self, analog_modulation_state: int) -> None:
        if analog_modulation_state == 1 or analog_modulation_state == 0:
            self.instrument.write(f"sames {analog_modulation_state}")

    def get_digital_modulation_state(self) -> int:
        return int(self.instrument.query("gdmes?"))

    def set_digital_modulation_state(self, digital_modulation_state: int) -> None:
        if digital_modulation_state == 1 or digital_modulation_state == 0:
            self.instrument.write(f"sames {digital_modulation_state}")

    def get_power(self) -> float:
        return float(self.instrument.query("p?"))

    def set_power(self, power: float) -> None:
        if power >= 0 and power <= self.max_power:
            self.instrument.write(f"p {power:.3f}")

    def get_current(self) -> float:
        return float(self.instrument.query("glc?"))

    def set_current(self, current: float) -> None:
        if current >= 0 and current <= self.max_current:
            self.instrument.write(f"slc {current:.2f}")

    def get_operating_mode(self) -> str:
        return self.instrument.query("gom?")

    def get_interlock_state(self) -> str:
        return self.instrument.query("ilk?")

    def get_operating_fault(self) -> str:
        return self.instrument.query("f?")

    def get_serial_number(self) -> int:
        return int(self.instrument.query("gsn?"))

    def get_laser_head_operating_hours(self) -> float:
        return float(self.instrument.query("hrs?"))

    # If autostart is enabled the autostart sequence will ‘Restart’.
    # If autostart is disabled, the laser will go through a forced autostart sequence.
    def laser_on_force_autostart(self) -> None:
        self.instrument.write("@cob1")

    # If autostart is enabled the start-up sequence will ‘Abort’.
    # If autostart is disabled all laser will go directly into an OFF state.
    def laser_off(self) -> None:
        self.instrument.write("@cob0")

    def enter_constant_power_mode(self) -> None:
        self.instrument.write("cp")

    def enter_constant_current_mode(self) -> None:
        self.instrument.write("ci")

    def enter_modulation_mode(self) -> None:
        self.instrument.write("em")

    # Watts
    def read_actual_output_power(self) -> float:
        return float(self.instrument.query("pa?"))

    # mA
    def read_actual_laser_current(self) -> float:
        return float(self.instrument.query("rlc"))

    def clear_fault(self) -> None:
        self.instrument.write("cf")


if __name__ == "__main__":
    laser = HuebnerCobolt06mld("laser", "ASRL3", 0.08, 250, 514)
    laser.enter_constant_power_mode()
    laser.set_status(1)
    laser.set_power(0.03)
    import time

    time.sleep(2)
    laser.set_status(0)
