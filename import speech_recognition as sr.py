import speech_recognition as sr
import pyttsx3
import random
from googletrans import Translator

# Инициализация распознавателя речи
r = sr.Recognizer()

# Инициализация синтезатора речи
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Настройка скорости речи (по желанию)

# Инициализация переводчика
translator = Translator()

# Язык по умолчанию
current_language = "ru"  # Изначально русский

# Функция для произношения текста
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для генерации ответа
def generate_response(user_input):
    global current_language
    
    if "привет" in user_input.lower() or "hello" in user_input.lower():
        return "Привет! Чем могу помочь?" if current_language == "ru" else "Hello! How can I help?"
    elif "как дела" in user_input.lower() or "how are you" in user_input.lower():
        return "Я просто программа, но всё хорошо, спасибо!" if current_language == "ru" else "I am just a program, but I'm fine, thank you!"
    elif "погода" in user_input.lower() or "weather" in user_input.lower():
        return "К сожалению, я не могу проверить погоду прямо сейчас. Пожалуйста, посмотрите в интернете!" if current_language == "ru" else "Unfortunately, I cannot check the weather right now. Please check it online!"
    elif "что ты умеешь" in user_input.lower() or "what can you do" in user_input.lower():
        return "Я могу распознавать вашу речь и отвечать на простые вопросы." if current_language == "ru" else "I can recognize your speech and answer simple questions."
    elif "стоп" in user_input.lower() or "stop" in user_input.lower():
        return "Завершаю работу." if current_language == "ru" else "I am stopping now."
    elif "переключись на русский" in user_input.lower():
        current_language = "ru"
        return "Переключился на русский язык."
    elif "switch to english" in user_input.lower():
        current_language = "en"
        return "Switched to English."
    elif "переведи" in user_input.lower() or "translate" in user_input.lower():
        word = user_input.split(" ", 1)[1] if len(user_input.split(" ", 1)) > 1 else ""
        if word:
            translated = translate_word(word)
            return translated
        else:
            return "Пожалуйста, скажите слово, которое нужно перевести."
    else:
        responses = [
            "Извините, я не совсем понял. Можете повторить?",
            "Пожалуйста, уточните ваш запрос.",
            "Я вас не понимаю, повторите, пожалуйста."
        ]
        return random.choice(responses)

# Функция для перевода слова
def translate_word(word):
    try:
        translated = translator.translate(word, src=current_language, dest="en" if current_language == "ru" else "ru")
        return f"Перевод слова '{word}': {translated.text}" if current_language == "ru" else f"Translation of '{word}': {translated.text}"
    except Exception as e:
        return f"Ошибка при переводе: {str(e)}"

# Основной цикл работы
while True:
    with sr.Microphone() as source:
        print("Говорите...")
        # Удаление фонового шума
        r.adjust_for_ambient_noise(source)

        # Запись аудио с микрофона
        audio = r.listen(source)

    # Распознавание речи
    try:
        # Используем OpenAI Speech Recognition
        text = r.recognize_google(audio, language="ru-RU" if current_language == "ru" else "en-US")
        print("Вы сказали: " + text)
        
        # Генерация ответа
        response = generate_response(text)

        # Произнесение ответа
        print(f"Ответ: {response}")
        speak(response)

        # Если пользователь сказал "стоп", завершаем диалог
        if "стоп" in text.lower() or "stop" in text.lower():
            break

    except sr.UnknownValueError:
        print("Извините, я не понял, что вы сказали.")
        speak("Извините, я не понял, что вы сказали.")
    except sr.RequestError as e:
        print(f"Ошибка при запросе к сервису распознавания речи: {e}")
        speak(f"Ошибка при запросе к сервису распознавания речи: {e}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")
        speak(f"Произошла неизвестная ошибка: {e}")
