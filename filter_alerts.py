import json
import os

def main():
    filename = "events.json"
    if not os.path.exists(filename):
        print(f"Ошибка: Файл {filename} не найден!")
        return

    # Чтение событий из JSON-файла
    with open(filename, "r", encoding="utf-8") as f:
        events = json.load(f)

    # Фильтрация событий: оставляем только уровень critical
    critical_events = [e for e in events if e.get("level") == "critical"]

    # Вывод каждого критического события
    print("Список критических событий:")
    for event in critical_events:
        print(f"  - [{event['level'].upper()}] {event['message']}")
    
    # Финальный summary по требованию задания
    print(f"\nкритичных {len(critical_events)}")

if __name__ == "__main__":
    main()
