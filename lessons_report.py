import logging
import time

import requests
import telegram
from environs import Env

logger = logging.getLogger(__file__)


class TgLogHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def request_attempts(url, headers, params, timeout):
    response = requests.get(
        url, headers=headers, params=params, timeout=timeout
    )
    response.raise_for_status()

    return response.json()


def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger.addHandler(TgLogHandler(bot, chat_id))
    logger.info("Бот запущен")

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
        ) as err:
            logger.info("Бот упал с ошибкой:")
            logger.error(err)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    api_token = env("DVMN_API_TOKEN")
    bot_token = env("TG_BOT_TOKEN")
    chat_id = env("TG_CHAT_ID")
    request_timeout = env.int("REQUEST_TIMEOUT")

    bot = telegram.Bot(bot_token)
    main()
