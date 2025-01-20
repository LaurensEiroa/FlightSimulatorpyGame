
from src.Flight_simulator.drone import Drone
from src.Flight_simulator.GUI import FlightSimulator

if __name__=="__main__":
    drone = Drone()
    simulator = FlightSimulator(objects=[drone])
    simulator.run()