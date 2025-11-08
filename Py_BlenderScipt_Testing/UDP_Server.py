import bpy
import socket
import json
UDP_IP = "127.0.0.1"
PORT_TX = 8000  # Port to send to Unity

sock_tx = None


def setup_sockets():
    """Initialize UDP socket for sending"""
    global sock_tx
    sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP socket setup complete.")


def send_data(message):
    """Send data to Unity"""
    global sock_tx
    if not sock_tx:
        print("Socket not set up yet. Call setup_sockets() first.")
        return
    try:
        sock_tx.sendto(message.encode("utf-8"), (UDP_IP, PORT_TX))
        print(f"Sent: {message}")
    except Exception as e:
        print(f"Error sending: {e}")


def stop_communication():
    """Close UDP socket"""
    global sock_tx
    if sock_tx:
        sock_tx.close()
        sock_tx = None
        print("UDP socket closed.")
