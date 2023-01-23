import json
from time import time
from sys import stderr

import requests
from random import choice, randint
from loguru import logger

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>")


class FailCreateSessionException(Exception):
    """
    Raised when DiscordAccount object failed to create account session using requests library
    """
    pass


class NoChatAccessException(Exception):
    """
    Raised when discord API response status code in not 200 during checking chat access
    """
    pass


class FailCheckChatAccessException(Exception):
    """
    Raised when DiscordAccount object failed to check chat access
    """
    pass


class UnauthSendMessageException(Exception):
    """
    Raised when discord API response status code in not 200 during sending message
    """
    pass


class DiscordAccount:
    def __init__(self, name: str, token: str, proxy: str, useragent: str, chat_id: str, messages: list,
                 min_delay_sec: int, max_delay_sec: int, start_on_launch: bool, loop: bool):
        self.name = name
        self.token = token
        self.proxy = proxy
        self.useragent = useragent
        self.chat_id = chat_id
        self.messages = messages
        self.min_delay_sec = min_delay_sec
        self.max_delay_sec = max_delay_sec
        self.start_on_launch = start_on_launch
        self.loop = loop
        self.next_message_timestamp = time() if self.start_on_launch else self.__generate_next_message_timestamp()

        self.account_session = self.__generate_account_session()
        self.__check_chat_access()

    def __generate_account_session(self):
        try:
            session = requests.Session()
            headers = {
                'user-agent': self.useragent,
                'authorization': self.token
            }
            proxies = {
                'http': self.proxy,
                'https': self.proxy
            }
            session.headers = headers
            session.proxies = proxies
            return session

        except Exception:
            raise FailCreateSessionException

    def __check_chat_access(self):

        try:
            url = f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=2'
            response = self.account_session.get(url)

            if response.status_code != 200:
                raise NoChatAccessException

        except Exception:
            raise FailCheckChatAccessException

    def __generate_next_message_timestamp(self) -> dict:
        return time() + randint(self.min_delay_sec, self.max_delay_sec)

    def send_message(self) -> requests.Response:
        self.next_message_timestamp = self.__generate_next_message_timestamp()

        random_message = choice(self.messages)
        data = {
            'content': random_message,
            'tts': False
        }
        url = f'https://discord.com/api/v9/channels/{self.chat_id}/messages'
        response = self.account_session.post(url, json=data)

        if response.status_code != 200:
            raise UnauthSendMessageException

        return json.loads(response.text)


