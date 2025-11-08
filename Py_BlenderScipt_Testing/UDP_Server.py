import bpy
import socket
import json

UDP_IP = "127.0.0.1"
PORT_TX = 8000  # Port to send to Unity

_sock_tx = None  # use underscore to mark as internal


def setup_sockets():
    """Initialize UDP socket for sending"""
    global _sock_tx
    if _sock_tx is not None:
        print("UDP socket already set up.")
        return
    try:
        _sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _sock_tx.setblocking(False)  # prevents Blender UI hangs
        print(f"UDP socket setup complete. Sending to {UDP_IP}:{PORT_TX}")
    except Exception as e:
        print(f"Failed to create UDP socket: {e}")


def send_data(message):
    """Send data to Unity"""
    global _sock_tx
    if not _sock_tx:
        print("Socket not set up yet. Call setup_sockets() first.")
        return

    try:
        # Ensure it's bytes
        if isinstance(message, dict):
            message = json.dumps(message)
        if isinstance(message, str):
            message = message.encode("utf-8")

        _sock_tx.sendto(message, (UDP_IP, PORT_TX))
        print(f"Sent UDP packet ({len(message)} bytes) to {UDP_IP}:{PORT_TX}")
    except Exception as e:
        print(f"Error sending UDP data: {e}")


def stop_communication():
    """Close UDP socket"""
    global _sock_tx
    if _sock_tx:
        try:
            _sock_tx.close()
            print("UDP socket closed.")
        except Exception as e:
            print(f"Error closing socket: {e}")
        finally:
            _sock_tx = None
    else:
        print("UDP socket not active.")
