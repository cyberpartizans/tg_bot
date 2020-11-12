from telethon import TelegramClient  # type: ignore
from telethon.errors import SessionPasswordNeededError  # type: ignore
from .read_config import read_config


async def get_telegram_client() -> TelegramClient:
    """

    :return:
    """
    client_name, api_id, api_hash, phone_number = read_config()
    client = TelegramClient(client_name, api_id, api_hash)
    await client.start()
    return client


async def authorize(client: TelegramClient) -> None:
    """

    :param client:
    :return:
    """
    client_name, api_id, api_hash, phone_number = read_config()

    # убедитесь, что вы авторизованы
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
