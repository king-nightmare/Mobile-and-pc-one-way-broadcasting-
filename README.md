# Local Network UDP Broadcast Chat

A lightweight, terminal-based Python application that utilizes the **UDP (User Datagram Protocol)** to broadcast messages to all devices sharing the same local area network (LAN). 

It features a continuous input loop on the broadcaster side and an active listener on the client side.

## 🚀 How It Works

Because this script uses UDP (`SOCK_DGRAM`) and the global broadcast address (`255.255.255.255`), the broadcaster doesn't need to connect to a specific receiver IP. It simply shouts the message out into the network, and any client listening on the designated port (`50000`) will catch it and display it.

---

## 🛠️ Installation & Requirements

* **Python 3.x** installed on your system.
* No external libraries are required! The project relies entirely on Python's built-in `socket` library.

---

## 💻 Usage

To test this locally or across multiple machines on the same Wi-Fi/LAN network, follow these steps:

### 1. Start the Client (Listener)
The client must be running so it can listen for incoming broadcasts. Run the client script in your terminal or command prompt:

```bash
python client.py


