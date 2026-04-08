import socket
import threading

clients = []  # список подключённых клиентов

def broadcast(message, sender):
    """Рассылает сообщение всем клиентам, кроме отправителя"""
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    """Обрабатывает сообщения от одного клиента"""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    """Запускает сервер"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('10.168.0.80', 8000))  # ваш IP и порт
    server.listen()
    print("Сервер запущен на 10.168.0.80:8000")

    while True:
        client_socket, addr = server.accept()
        print(f"Подключился клиент {addr}")
        clients.append(client_socket)
        # Запускаем отдельный поток для каждого клиента
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()

