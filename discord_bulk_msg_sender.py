from sys import stderr
from operator import attrgetter
from time import time, sleep
from ast import literal_eval

from pyfiglet import Figlet
from loguru import logger

from src.discord_account import *

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>")


f = Figlet(font='5lineoblique')
print(f.renderText('Busher'))
print('Telegram channel: @CryptoKiddiesClub')
print('Telegram chat: @CryptoKiddiesChat')
print('Twitter: @CryptoBusher\n')


def init_raw_accounts(_raw_accounts: list) -> list:
    _account_objects = []
    for account in _raw_accounts:
        try:
            split_account = account.split('|')
            _account_objects.append(DiscordAccount(
                name=split_account[0],
                token=split_account[1],
                proxy=split_account[2],
                useragent=split_account[3],
                chat_id=split_account[4],
                messages=literal_eval(split_account[5]),
                min_delay_sec=int(split_account[6]),
                max_delay_sec=int(split_account[7]),
                start_on_launch=True if split_account[8] == 'True' else False,
                loop=True if split_account[9] == 'True' else False
            ))

        except FailCreateSessionException:
            logger.error(f'Failed to init account, reason: failed to create requests session')
            with open('data/failed_accounts/failed_to_create_session.txt', 'a') as file:
                file.write(f'{account}\n')

        except NoChatAccessException:
            logger.error(f'Failed to init account, reason: no chat access')
            with open('data/failed_accounts/no_chat_access.txt', 'a') as file:
                file.write(f'{account}\n')

        except FailCheckChatAccessException:
            logger.error(f'Failed to init account, reason: failed to check chat access')
            with open('data/failed_accounts/failed_to_check_chat_access.txt', 'a') as file:
                file.write(f'{account}\n')

        except Exception as e:
            logger.error(f'Undefined error during account init, reason: {e}')
            with open('data/failed_accounts/undefined_errors.txt', 'a') as file:
                file.write(f'{account}\n')

    return _account_objects


def start_sending_messages(_account_objects: list[DiscordAccount]):
    while True:
        if not _account_objects:
            logger.success('Finished sending messages')
            break

        _account_objects.sort(key=attrgetter('next_message_timestamp'), reverse=False)

        for account in _account_objects:
            if account.next_message_timestamp <= time():
                try:
                    response = account.send_message()
                    logger.success(f'{account.name} - message sent, content: {response["content"][:20]}, '
                                   f'channel: {response["channel_id"]}')
                    if not account.loop:
                        _account_objects.remove(account)

                except UnauthSendMessageException as e:
                    logger.error(f'{account.name} - unauthorized, reason: {e}')

                except Exception as e:
                    logger.error(f'{account.name} - failed to send message, reason: {e}')

            else:
                sleep(2)
                break


if __name__ == '__main__':
    with open('data/accounts.txt') as f:
        raw_accounts = [line.rstrip() for line in f]
    logger.info(f'Uploaded {len(raw_accounts)} accounts')

    account_objects = init_raw_accounts(raw_accounts)
    logger.info(f'Initialized {len(account_objects)} accounts')

    start_sending_messages(account_objects)
