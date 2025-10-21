# original code
# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

## import UdpComms as U
## import time

## # Create UDP socket to use for sending (and receiving)
## sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

## i = 0

## while True:
##    sock.SendData('Sent from Python: ' + str(i) + 'Good Morning') # Send this string to other application
##    i += 1
##
##    data = sock.ReadReceivedData() # read data
##
##    if data != None: # if NEW data has been received since last ReadReceivedData function call
##        print(data) # print new received data
##
##    time.sleep(1)


#converted by claude AI
import bpy
import socket
import threading
import time

# Configuration
UDP_IP = "127.0.0.1"
PORT_TX = 8000  # Port to send to Unity
PORT_RX = 8001  # Port to receive from Unity

# Global variables
running = False
receive_thread = None
sock_tx = None
sock_rx = None
latest_data = None

def setup_sockets():
    """Initialize UDP sockets"""
    global sock_tx, sock_rx
    
    # Socket for sending to Unity
    sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Socket for receiving from Unity
    sock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_rx.bind((UDP_IP, PORT_RX))
    sock_rx.settimeout(0.1)  # Non-blocking with timeout
    
    print(f"Sockets initialized - Sending to {UDP_IP}:{PORT_TX}, Receiving on {UDP_IP}:{PORT_RX}")

def receive_data():
    """Thread function to continuously receive data"""
    global running, latest_data, sock_rx
    
    print("Receive thread started")
    
    while running:
        try:
            data, addr = sock_rx.recvfrom(1024)
            latest_data = data.decode('utf-8')
            print(f"Received: {latest_data}")
        except socket.timeout:
            # No data received, continue loop
            pass
        except Exception as e:
            print(f"Error receiving: {e}")
            time.sleep(0.1)
    
    print("Receive thread stopped")

def send_data(message):
    """Send data to Unity"""
    global sock_tx
    try:
        sock_tx.sendto(message.encode('utf-8'), (UDP_IP, PORT_TX))
    except Exception as e:
        print(f"Error sending: {e}")

def start_communication():
    """Start the UDP communication"""
    global running, receive_thread
    
    if running:
        print("Communication already running!")
        return
    
    setup_sockets()
    running = True
    
    # Start receive thread
    receive_thread = threading.Thread(target=receive_data, daemon=True)
    receive_thread.start()
    
    print("UDP Communication started")

def stop_communication():
    """Stop the UDP communication"""
    global running, sock_tx, sock_rx
    
    running = False
    
    if receive_thread:
        receive_thread.join(timeout=1.0)
    
    if sock_tx:
        sock_tx.close()
    if sock_rx:
        sock_rx.close()
    
    print("UDP Communication stopped")

# Example usage with Blender timer
counter = 0

def communication_loop():
    """Main communication loop - called by Blender timer"""
    global counter, latest_data
    
    # Send data to Unity
    message = bpy.context.scene
    send_data(message)
    counter += 1
    
    # Check for received data
    if latest_data:
        print(f"Latest from Unity: {latest_data}")
        # Reset after reading
        latest_data = None
    
    return 1.0  # Run again in 1 second

# Start/Stop operators for Blender UI
class StartUDPOperator(bpy.types.Operator):
    bl_idname = "wm.start_udp"
    bl_label = "Start UDP Communication"
    
    def execute(self, context):
        start_communication()
        # Register timer to run communication loop
        bpy.app.timers.register(communication_loop)
        return {'FINISHED'}

class StopUDPOperator(bpy.types.Operator):
    bl_idname = "wm.stop_udp"
    bl_label = "Stop UDP Communication"
    
    def execute(self, context):
        stop_communication()
        # Unregister timer
        if bpy.app.timers.is_registered(communication_loop):
            bpy.app.timers.unregister(communication_loop)
        return {'FINISHED'}

# Register operators
def register():
    bpy.utils.register_class(StartUDPOperator)
    bpy.utils.register_class(StopUDPOperator)

def unregister():
    bpy.utils.unregister_class(StartUDPOperator)
    bpy.utils.unregister_class(StopUDPOperator)
    stop_communication()

if __name__ == "__main__":
    register()
    
    # Auto-start (comment out if you want manual control)
    start_communication()
    bpy.app.timers.register(communication_loop)