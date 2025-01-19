import asyncio
import websockets
import time
from config import Config

async def pi_zero_request(rpi_name,instruction):

    uri = f"ws://{Config.IPs[rpi_name]}:{Config.WEBSOCKET_PORT}"  

    async with websockets.connect(uri) as websocket:
        print("Connection from pi 5 to Zero established")
        print(f"sending instruction to {room}({Config.IPs[rpi_name]}): {instruction}") 

        await websocket.send(instruction) 
        message = await websocket.recv() 

        # Receive one message per instruction 
        print(f"Received message on server: {message}") 
        if instruction=="read_bmp":
            temperature, pressure, altitude = message.split("-")
            return temperature, pressure, altitude
        if instruction=="read_mpu":
            acceleration, gyro, temperature = message.split("-")
            return acceleration, gyro, temperature
        return message

if __name__=="__main__":
    room = "zero4"
    instructions = ["read_acc","read_gyr"]
    asyncio.get_event_loop().run_until_complete(pi_zero_request(room,instructions))