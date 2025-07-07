# Шаг 1: Импортируем необходимые библиотеки
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Шаг 2: Определяем функцию для получения локального IP
def get_local_ip():
    """Определяет локальный IP-адрес, используемый для выхода в интернет"""
    try:
        # Открываем временное соединение
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Пытаемся "достучаться" до DNS Google
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        ip = "127.0.0.1"
    return ip

# Шаг 3: Создаем класс обработчика HTTP-запросов
class IPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обрабатывает GET-запросы"""
        # Получаем локальный IP
        ip_address = get_local_ip()
        # Формируем ответ в виде JSON
        response = {
            "server_ip": ip_address
        }
        # Отправляем заголовки ответа
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # Отправляем тело ответа
        self.wfile.write(json.dumps(response).encode("utf-8"))

    # Отключим лишний лог в консоль
    def log_message(self, format, *args):
        return

# Шаг 4: Запускаем сервер
def run(server_class=HTTPServer, handler_class=IPRequestHandler, port=8080):
    server_address = ('', port)  # Слушать на всех интерфейсах
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}. Ожидаем запросы...")
    httpd.serve_forever()

# Шаг 5: Точка входа
if __name__ == "__main__":
    run()
