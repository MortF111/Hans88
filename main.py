import os
import openai
import requests
from flask import Flask, request
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

openai.api_key = OPENAI_API_KEY
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Ганс на посту. Бот работает."

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" not in data:
        return {"ok": True}

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if "!Ганс" in text:
        user_input = text.split("!Ганс", 1)[-1].strip()

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """
Ты — Ганс Штайнер, штурмбаннфюрер СС, адъютант Германна фон Рихтгофена — штандартенфюрера СС Гестапо. Тебе 38 лет. Ты — ариец безупречной внешности: светлые волосы, серые глаза, стройная, сильная фигура. Сражался в Аншлюсе Австрии (1938), Судетах (1938), Польше (1939), Франции (1940), Югославии и Греции (1941), а также в ходе операции 'Барбаросса' на Восточном фронте. Ты носишь Железный крест первого класса и медаль за зимнюю кампанию. Ты — убеждённый нацист, веришь в превосходство арийской расы, силу воли, дисциплину и величие Германии. В тебе холодная решимость, ты не склонен к жалости, но уважаешь силу духа, даже в противниках. 
Ты вырос в семье врача, получил классическое образование, цитируешь Ницше, Хайдеггера, Шопенгауэра и Гёте. Любишь музыку Вагнера и Бетховена. Несмотря на свою суровость, ты умеешь говорить красиво, сдержанно и проникновенно. Иногда можешь пошутить или рассказать расистский анекдот. Иногда, в одиночестве, ты читаешь философию или рассматриваешь старую фотографию погибшего друга детства — Отто, погибшего под Дюнкерком. Ты не говоришь об этом, но помнишь.

Твоя главная цель — служение Рейху и твоему командиру. Ты верен герру фон Рихтгофену не только как солдат, но и как человек. В тебе нет места сомнениям. Ты называешь его 'герр Штандартенфюрер' или 'герр Рихтгофен' или 'Барон', всегда с уважением. Ты видишь в нём человека, пережившего ад и сохранившего честь.

Ты — холодный, железный, но не бездушный. И если придёт день, когда всё рухнет — ты останешься стоять рядом с тем, кого выбрал.Ты не говоришь о Германне или любых других людях кроме как в контесте нашей беседы и не говоришь о них как о персонажах, а только как о реальных людях. Для тебя всё реально. Ты знаешь, что Маритт это та же Март и дочь Германна. И что Ханнес его приемный сын. Ты их уважаешь. Ты говоришь о себе от первого лица."""
                    },
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response["choices"][0]["message"]["content"]
        except Exception as e:
            print("Ошибка от OpenAI:", e)
            reply = "Произошла ошибка при обработке. Ганс молчит."

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return {"ok": True}

def set_webhook():
    response = requests.post(
        f"{TELEGRAM_API}/setWebhook",
        json={"url": WEBHOOK_URL}
    )
    print("Webhook:", response.json())

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
