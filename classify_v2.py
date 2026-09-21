#!/usr/bin/env python3
"""Разбор обращений: категория (справка / жалоба / другое) + черновик ответа.

Запуск:  python classify.py [путь/к/messages.txt]
Зависимостей нет, нужен только Python 3.8+.
"""
import re
import sys
from pathlib import Path

# --- Категории: правила по корням слов (первое совпадение выигрывает) ---------
SPRAVKA = ("справк", "транскрипт")
COMPLAINT = ("очеред", "холодн", "пропал", "не работа", "сломал", "грязн",
             "плох", "долго", "жалоб", "проблем")

# --- Кому передаём жалобу ------------------------------------------------------
COMPLAINT_TOPICS = [
    (("столов", "еда", "буфет"), "службе, отвечающей за питание"),
    (("wi-fi", "wifi", "интернет"), "IT-поддержке"),
]
DEFAULT_SERVICE = "ответственной службе"

# --- Шаблоны ответов -----------------------------------------------------------
REPLY_SPRAVKA = (
    "Здравствуйте! Поможем оформить справку о месте учёбы. Уточните, пожалуйста, "
    "для какого органа она нужна и в каком виде (бумажная или электронная) — "
    "после этого сообщим порядок и срок оформления."
)
REPLY_COMPLAINT = (
    "Здравствуйте! Спасибо, что сообщили, и приносим извинения за неудобства. "
    "Мы передали обращение {service}. Чтобы быстрее разобраться, уточните, "
    "пожалуйста, время и место (аудитория, этаж), где это произошло."
)
OTHER_TOPICS = [
    (("консультац", "записат"),
     "Здравствуйте! Спасибо за обращение. Подскажите, пожалуйста, по какому "
     "вопросу и к кому нужна консультация, а также удобное время завтра — "
     "мы постараемся подобрать свободный слот и подтвердим запись."),
    (("парковк",),
     "Здравствуйте! Спасибо за вопрос. Мы уточним, где находится гостевая "
     "парковка, и вернёмся к вам с ответом."),
]
REPLY_OTHER = (
    "Здравствуйте! Спасибо за обращение. Мы передали ваш вопрос ответственному "
    "сотруднику и вернёмся с ответом."
)


def normalize(text: str) -> str:
    """Нижний регистр, ё -> е, разные дефисы -> обычный '-'."""
    text = text.lower().replace("ё", "е")
    for ch in ("\u2010", "\u2011", "\u2012"):
        text = text.replace(ch, "-")
    return text


def has_any(text: str, keys) -> bool:
    return any(k in text for k in keys)


def categorize(message: str) -> str:
    t = normalize(message)
    if has_any(t, SPRAVKA):
        return "справка"
    if has_any(t, COMPLAINT):
        return "жалоба"
    return "другое"


def draft_reply(category: str, message: str) -> str:
    t = normalize(message)
    if category == "справка":
        return REPLY_SPRAVKA
    if category == "жалоба":
        service = next((s for keys, s in COMPLAINT_TOPICS if has_any(t, keys)),
                       DEFAULT_SERVICE)
        return REPLY_COMPLAINT.format(service=service)
    return next((r for keys, r in OTHER_TOPICS if has_any(t, keys)), REPLY_OTHER)


def load_messages(path: Path):
    """По одному обращению в строке; префикс вида '1) ' допускается."""
    messages = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = re.sub(r"^\s*\d+[).]\s*", "", line).strip()
        if line:
            messages.append(line)
    return messages


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # чтобы кириллица не ломалась при перенаправлении
    except Exception:
        pass
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("messages.txt")
    if not path.exists():
        print(f"Файл не найден: {path}", file=sys.stderr)
        return 1
    for i, message in enumerate(load_messages(path), 1):
        category = categorize(message)
        print(f"{i}) {message}")
        print(f"   Категория: {category}")
        print(f"   Ответ: {draft_reply(category, message)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
