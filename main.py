import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random

# Словарь: русское слово -> английский перевод
words_dict = {
    "легко": {
        "кот": "cat",
        "собака": "dog", 
        "солнце": "sun",
        "фокус": "focus",
        "урок": "lesson",
        "зеленый": "green",
        "красный": "red",
        "синий": "blue",
        "черный": "black"
    },
    "средне": {
        "лето": "summer",
        "школа": "school",
        "навык": "skill",
        "автобус": "bus",
        "самолет": "plane",
        "вертолет": "helicopter"
    },
    "тяжело": {
        "технология": "technology",
        "информация": "information",
        "друг": "friend",
        "обучение": "training",
        "стратегия": "strategy",
        "вызов": "challenge",
        "проблема": "problem"
    }
}

points = {
    "легко": 1,
    "средне": 3,
    "тяжело": 5
}

current_seria = 0
max_seria = 0
total_points = 0
duration = 5
sample_rate = 16000

print("Это игра произнеси правильно слово!")
print("Твоя задача выбрать сложность легко, средне или тяжело, за каждый уровень дают больше очков от легной до сложной")
print("Тебе покажут русское слово, а ты должен произнести его английский перевод!")

while True:
    level = input("Выберете сложность:")

    if level in words_dict:
        # Выбираем случайное русское слово и его английский перевод
        russian_word = random.choice(list(words_dict[level].keys()))
        english_word = words_dict[level][russian_word]
    else:
        print("Не удалось распознать сложность.")
        continue

    print(f"Рандомное слово из сложности '{level}': {russian_word}")
    print("Готовьтесь... говорите через 2 секунды")

    import time
    time.sleep(2)
    
    print("🎤 Говорите сейчас английский перевод!")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...")

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    
    try:
        with sr.AudioFile("output.wav") as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)

            text = recognizer.recognize_google(audio, language="en-US")
            print("Ты сказал:", text)
            
            # Проверяем, сказал ли игрок правильный английский перевод
            if text.lower().strip() == english_word.lower():
                total_points += points[level]
                print(f"✅ Правильно! Вы получили +{points[level]} баллов")
                current_seria += 1
                if current_seria > max_seria:
                    max_seria = current_seria
                print(f"💰 Всего баллов: {total_points}")
                print(f"🔥 Текущая серия: {current_seria} правильных подряд")
                print(f"🏆 Рекорд серии: {max_seria}")
            else:
                print(f"❌ Неправильно. Вы сказали: '{text}', а нужно: '{english_word}'")
                current_seria = 0
                
    except sr.UnknownValueError:
        print("❌ Не удалось распознать речь. Попробуйте говорить четче.")
        current_seria = 0
    except sr.RequestError as e:
        print(f"🚫 Ошибка сервиса: {e}")
        print("Проверьте интернет-соединение")
    
    play_again = input("\nХотите продолжить игру? (да/нет): ").lower()
    if play_again != "да":
        print(f"\n🎮 Игра завершена!")
        print(f"💰 Ваш итоговый счет: {total_points} баллов")
        print(f"🏆 Самая длинная серия: {max_seria} правильных подряд")
        break
