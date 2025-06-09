import os
import subprocess
from PIL import Image

# Введення коду товару
product_code = input("🔢 Введи код товару (наприклад 12411): ").strip()

# Параметри
input_folder = "input_images"
output_folder = os.path.join(os.getcwd(), product_code)
target_width = 1800
quality = 90

# Створення вихідної директорії
os.makedirs(output_folder, exist_ok=True)

# Обробка файлів
image_urls = []
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with Image.open(input_path) as img:
            # Зміна розміру, якщо потрібно
            if img.width > target_width:
                width_percent = target_width / float(img.width)
                new_height = int(float(img.height) * width_percent)
                img = img.resize((target_width, new_height), Image.LANCZOS)

            # Конвертація PNG → JPG при потребі
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Збереження
            img.save(output_path, optimize=True, quality=quality)

            # Додавання посилання
            img_url = f"https://github.com/essenceclothes/product-images/blob/main/{product_code}/{filename}?raw=true"
            image_urls.append(img_url)

        print(f"✅ Оброблено: {filename}")

# Git команди
try:
    subprocess.run(["git", "add", product_code], check=True)
    subprocess.run(["git", "commit", "-m", f"Add product images for {product_code}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("🚀 Зображення запушено в GitHub.")
except subprocess.CalledProcessError:
    print("❌ Сталася помилка під час git push. Перевір доступ і репозиторій.")

# Вивід результату
print("\n📎 Прямі посилання на зображення:")
print(";".join(image_urls))
