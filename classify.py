import os

# База готовых ответов на русском языке
RESPONSES = {
    "справка": "Здравствуйте! Данную справку вы можете заказать в личном кабинете студента или обратиться в МФЦ / деканат.",
    "жалоба": "Здравствуйте! Спасибо за сигнал. Мы передали вашу жалобу в соответствующую службу для оперативного исправления ситуации.",
    "другое": "Здравствуйте! Для уточнения деталей или записи, пожалуйста, свяжитесь с ответственным отделом или воспользуйтесь онлайн-формой."
}

def classify_message(text):
    text_lower = text.lower()
    # Логика классификации по ключевым словам
    if "справк" in text_lower or "где" in text_lower or "как" in text_lower:
        return "справка"
    elif "очередь" in text_lower or "холодн" in text_lower or "пропал" in text_lower or "wi-fi" in text_lower:
        return "жалоба"
    else:
        return "другое"

def main():
    filename = "messages.txt"
    if not os.path.exists(filename):
        print(f"Ошибка: Файл {filename} не найден!")
        return

    with open(filename, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    for i, msg in enumerate(messages, 1):
        category = classify_message(msg)
        draft = RESPONSES[category]
        
        print(f"Обращение №{i}: \"{msg}\"")
        print(f"  Категория: {category.upper()}")
        print(f"  Черновик ответа: {draft}")
        print("-" * 50)

if __name__ == "__main__":
    main()
