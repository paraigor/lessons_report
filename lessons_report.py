import time
from pprint import pprint

import requests
import telegram
from environs import Env


def request_attempts(url, headers, params, timeout):
    response = requests.get(
        url, headers=headers, params=params, timeout=timeout
    )
    response.raise_for_status()

    return response.json()


def main():
    env = Env()
    env.read_env()

    api_token = env("API_TOKEN")
    bot_token = env("BOT_TOKEN")
    chat_id = env("CHAT_ID")
    request_timeout = env.int("REQUEST_TIMEOUT")

    bot = telegram.Bot(bot_token)

    header = {"Authorization": f"Token {api_token}"}
    url = "https://dvmn.org/api/long_polling/"

    curr_timestamp = time.time()
    payload = {"timestamp": curr_timestamp}

    while True:
        try:
            response = request_attempts(url, header, payload, request_timeout)
            pprint(response)
            if response["status"] == "found":
                lesson_attempt = response["new_attempts"][0]
                if lesson_attempt["is_negative"]:
                    attempt_result = "К сожалению, в работе нашлись ошибки."
                else:
                    attempt_result = "Преподавателю все понравилось, можно приступать к следующему уроку!"

                message = f"""
                    У вас проверили работу «{lesson_attempt["lesson_title"]}»
                    {lesson_attempt["lesson_url"]}

                    {attempt_result}
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
