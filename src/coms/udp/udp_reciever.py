import socket
import cv2
import numpy as np
from config import Config
import asyncio

class UDPReceiver:
    def __init__(self, receiver_ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((receiver_ip, port))

    async def receive_data(self, data_type="image"):
        print("recieving data")
        buffer = b''
        max_dgram = Config.MAX_DGRAM_FRAME if data_type == "frame" else Config.MAX_DGRAM_DATA
        for _ in range(0, max_dgram):
            packet, _ = self.server_socket.recvfrom(max_dgram)
            buffer += packet
            if len(packet) < max_dgram:
                break
        return buffer

async def run():
    receiver = 'windows_computer'  # Replace with your receiver IP address

    udp_data_receiver = UDPReceiver(receiver_ip=Config.IPs[receiver], port=Config.UDP_DATA_PORT)
    #udp_frame_receiver = UDPReceiver(receiver_ip=Config.IPs[receiver], port=Config.UDP_FRAME_PORT)

    while True:
        #frame_data = await udp_frame_receiver.receive_data(data_type="frame")
        #frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        data = await udp_data_receiver.receive_data(data_type="data")
        data = data.decode('utf-8')

        print(f"recieved {data}")

        # Overlay the received data onto the frame
        #cv2.putText(frame, data, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the frame with the overlay
        #cv2.imshow('Received Frame', frame)

        # Break the loop on 'q' key press
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
