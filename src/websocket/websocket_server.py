import asyncio
import websockets
import time

class Config:
       IPs = {"ubuntu_laptop":"192.168.129.24",
              "pi5":"192.168.129.11",
              "piZero1":"192.168.129.14",
              "piZero2":"192.168.129.15",
              "piZero3":"192.168.129.22",
              "piZero4":"192.168.129.21"
              }
       APP_PORT = 8000
       UDP_PORT = 0000
       HTTP_PORT = 1111
       WEBSOCKET_PORT = 2222

       UDP_MAX_DGRAM = 2**15


async def pi_zero_request(rpi_name,instruction):

    uri = f"ws://{Config.IPs[rpi_name]}:{Config.WEBSOCKET_PORT}"  

    async with websockets.connect(uri) as websocket:
        print("Connection from pi 5 to Zero established")
        print(f"sending instruction to {rpi_name}({Config.IPs[rpi_name]}): {instruction}") 

        await websocket.send(instruction) 
        message = await websocket.recv() 

        # Receive one message per instruction 
        print(f"Received message on server: {message}") 
        if instruction=="read_bmp":
            temperature, pressure, altitude = message.split("/")
            return temperature, pressure, altitude
        if instruction=="read_mpu":
            acceleration, gyro, temperature = message.split("/")
            return acceleration, gyro, temperature
        return message
    
async def run():
    room = "piZero4"
    instructions = ["read_bmp","read_mpu"]
    while True:

        acc,gyr,T = await pi_zero_request(room,instructions[1])
        print(f"Acceleratio is: {acc}")
        print(f"Acceleratio is: {gyr}")
        print(f"Acceleratio is: {T}")
        print(f"---------------------")
        break

if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(run())