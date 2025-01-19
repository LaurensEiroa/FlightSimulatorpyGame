import asyncio
import websockets
import time
import ast

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
        #print("Connection from pi 5 to Zero established")
        #print(f"sending instruction to {rpi_name}({Config.IPs[rpi_name]}): {instruction}") 
        await websocket.send(instruction) 
        message = await websocket.recv() 

        # Receive one message per instruction 
        #print(f"Received message on server: {message}") 
        if instruction=="read_bmp":
            temperature, pressure, altitude = message.split("/")
            return temperature, pressure, altitude
        if instruction=="read_mpu":
            acceleration, gyro, temperature = message.split("/")
            return acceleration, gyro, temperature
        return message
    
async def run():
    import pandas as pd
    data = []
    columns = ["ax","ay","az","vrx,vry,vrz"]
    room = "piZero4"
    instructions = ["read_bmp","read_mpu"]
    t=-1
    while True:
        t+=1
        if t == 1000:
            break
        acc_raw,gyr_raw,T = await pi_zero_request(room,instructions[1])
        acc = acc_raw[1:-1].split(",")
        gyr = gyr_raw[1:-1].split(",")
        data.append([float(acc[0]),float(acc[1]),float(acc[2]),float(gyr[0]),float(gyr[1]),float([gyr[2]])])

    df = pd.DataFrame(data=data,columns=columns)
    df["ax"].plot()
        

if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(run())