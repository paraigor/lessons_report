import logging
import time

import requests
import telegram
from environs import Env

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


def request_attempts(url, headers, params, timeout):
    response = requests.get(
        url, headers=headers, params=params, timeout=timeout
    )
    response.raise_for_status()

    return response.json()


def main():
    logger.info("Бот запущен")

    env = Env()
    env.read_env()

    api_token = env("DVMN_API_TOKEN")
    bot_token = env("TG_BOT_TOKEN")
    chat_id = env("TG_CHAT_ID")
    request_timeout = env.int("REQUEST_TIMEOUT")

    bot = telegram.Bot(bot_token)

    header = {"Authorization": f"Token {api_token}"}
    url = "https://dvmn.org/api/long_polling/"

    curr_timestamp = time.time()
    payload = {"timestamp": curr_timestamp}

    while True:
        try:
            response = request_attempts(url, header, payload, request_timeout)

            if response["status"] == "found":
                lesson_attempt = response["new_attempts"][0]
                attempt_result = {
                    True: "Преподавателю все понравилось, можно приступать к следующему уроку!",
                    False: "К сожалению, в работе нашлись ошибки.",
                }
                message = f"""
                    У вас проверили работу «{lesson_attempt["lesson_title"]}»
                    {lesson_attempt["lesson_url"]}

                    {attempt_result[lesson_attempt["is_negative"]]}
                    """

                bot.send_message(chat_id=chat_id, text=message)

            payload = {
                "timestamp": response.get("timestamp_to_request")
                or lesson_attempt["timestamp"]
            }

        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
        ):
            continue


if __name__ == "__main__":
    main()
