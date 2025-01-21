
from src.Flight_simulator.drone import Drone
from src.Flight_simulator.GUI import FlightSimulator
import asyncio


if __name__=="__main__":
    print("starting drone")
    drone = Drone(receiver="windows_computer")
    print("starting simulator")
    simulator = FlightSimulator(objects=[drone])
    print("starting loop")
    asyncio.get_event_loop().run_until_complete(simulator.run())
