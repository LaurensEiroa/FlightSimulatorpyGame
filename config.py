# config.py
class Config:
       IPs = {"ubuntu_laptop":     "192.168.129.24",
              "windows_computer":  "192.168.129.5",
              "pi5":               "192.168.129.11",
              "piZero1":           "192.168.129.14",
              "piZero2":           "192.168.129.15",
              "piZero3":           "192.168.129.22",
              "piZero4":           "192.168.129.21"
              }
       
       UDP_DATA_PORT = 8010 
       UDP_FRAME_PORT = 8020
       WEBSOCKET_PORT = 8000

       MAX_DGRAM_FRAME = 2**15  # 32,768 bytes for frames
       MAX_DGRAM_DATA = 1024  # 1,024 bytes for data

       
       SENDER = "piZero4"
       RECIEVER = "ubuntu_laptop"
