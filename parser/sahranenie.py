env_content = """USERNAME=zatura55@mail.ru
PASSWORD=Masa34!masa35!
"""

with open(".env", "w") as file:
    file.write(env_content)

print("✅ Файл .env создан!")
