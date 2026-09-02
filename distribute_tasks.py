import os
import random
import requests

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# Укажите реальные Slack Member ID в формате "<@ID>" (как их найти — в Шаге 3)
TEAM_MEMBERS = [
    "U0AETCD18CD",
    "U03U1D7D1NG",
    "U076AJKLG5S",
    "U0B4Y4GH9RB"
]

RAW_CASES = {
    "3.1 Игровой интерфейс": [
        "Карта и навигация", "Инвентарь + панель быстрого доступа", 
        "Лодаут", "Вынос стартовых задач в HUD", "Кастомизация HUD"
    ],
    "3.2 Геймплей": [
        "Передвижение", "Камера", "Оружие", "Регдолл", "Смерть персонажа", 
        "Инвентарь", "Эмоции", "Никнейм", "Синхронизация", "Фоторежим", 
        "Зоны", "Контекстные взаимодействия"
    ],
    "3.3 Транспорт": [
        "Вызов транспорта", "Взаимодействие с транспортом", "Парковка", 
        "Девспаун транспорта", "Расход бензина", "Получение урона транспортом", 
        "Прострел колес", "Износ транспорта", "Автоматическая посадка владельцем", 
        "Возврат транспорта на дорогу", "Звуки транспорта", "Хелпер заезда на склоны", 
        "Near mode и Middle mode", "Выбор схемы управления"
    ],
    "3.4 Гараж и Кастомизация": [
        "Тюнинг стор", "Гараж", "Доп ресур. Универсальная деталь слияния", "Продажа транспорта"
    ],
    "3.5 Связь и Системные": [
        "Радио", "Проигрыватели", "Голосовой чат", "Рация", 
        "Системное окно", "Тайминги нажатия на иконку микрофона"
    ],
    "3.6 Билд": [
        "Накат билда"
    ]
}

def build_and_send_distribution():
    if not SLACK_WEBHOOK_URL:
        print("Ошибка: Ссылка SLACK_WEBHOOK_URL не найдена в Secrets!")
        return

    flat_list = []
    for section, items in RAW_CASES.items():
        for item in items:
            flat_list.append(f"[{section}] {item}")

    random.shuffle(flat_list)

    assignments = {member: [] for member in TEAM_MEMBERS}
    for index, task in enumerate(flat_list):
        assigned_person = TEAM_MEMBERS[index % len(TEAM_MEMBERS)]
        assignments[assigned_person].append(task)

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚀 Распределение кейсов на текущий релиз",
                "emoji": True
            }
        },
        {"type": "divider"}
    ]

    for member, tasks in assignments.items():
        task_text = "\n".join([f"• {t}" for t in tasks])
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Ответственный:* {member} (всего кейсов: {len(tasks)})\n{task_text}"
            }
        })
        blocks.append({"type": "divider"})

    payload = {"blocks": blocks}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("Сообщение успешно отправлено в Slack!")
    else:
        print(f"Ошибка отправки: {response.status_code}, {response.text}")

if __name__ == "__main__":
    build_and_send_distribution()
