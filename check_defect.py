import sys
import os
from PIL import Image

def analyze_image(image_path):
    if not os.path.exists(image_path):
        print(f"Ошибка: Файл {image_path} не найден!")
        return

    try:
        # Открываем изображение и переводим в режим RGB
        img = Image.open(image_path).convert('RGB')
        pixels = list(img.getdata())
        
        red_pixels_count = 0
        total_pixels = len(pixels)

        # Считаем пиксели, где красный цвет преобладает
        for r, g, b in pixels:
            if r > 150 and g < 100 and b < 100:
                red_pixels_count += 1

        # Если более 10% изображения — красное, это дефект
        red_ratio = red_pixels_count / total_pixels
        if red_ratio > 0.10:
            print("DEFECT")
        else:
            print("OK")

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")

if __name__ == "__main__":
    # Скрипт принимает путь к файлу в качестве аргумента командной строки
    if len(sys.argv) < 2:
        print("Использование: python check_defect.py <путь_к_картинке>")
        print("Пример: python check_defect.py ok.png")
    else:
        analyze_image(sys.argv[1])
