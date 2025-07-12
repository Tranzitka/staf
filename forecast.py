import random
from datetime import datetime

sports = ['Футбол', 'Теннис', 'Хоккей', 'Баскетбол', 'Бейсбол']
matches = {
    'Футбол': ['Арсенал vs Челси', 'Реал vs Атлетико'],
    'Теннис': ['Федерер vs Надаль', 'Синнер vs Алькарас'],
    'Хоккей': ['СКА vs Динамо', 'Рейнджерс vs Бостон'],
    'Баскетбол': ['Лейкерс vs Денвер', 'Голден Стэйт vs Милуоки'],
    'Бейсбол': ['Янкис vs Доджерс', 'Метс vs Ред Сокс']
}

def get_forecast():
    sport = random.choice(sports)
    match = random.choice(matches[sport])
    confidence = random.randint(60, 85)
    date = datetime.now().strftime('%d.%m.%Y')
    return (
        f"📅 Дата: {date}\n"
        f"🏟 Вид спорта: {sport}\n"
        f"🎯 Матч: {match}\n"
        f"✅ Прогноз: Победа первой команды\n"
        f"💡 Уверенность: {confidence}%"
    )
