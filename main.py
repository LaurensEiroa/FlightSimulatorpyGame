
from src.Flight_simulator.drone import Drone
from src.Flight_simulator.GUI import FlightSimulator
import asyncio


if __name__=="__main__":
    drone = Drone(receiver="ubuntu_laptop")
    simulator = FlightSimulator(objects=[drone])
    asyncio.get_event_loop().run_until_complete(simulator.run())
