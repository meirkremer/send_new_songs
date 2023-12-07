import datetime
from configuration import my_conf
from telethon.sync import TelegramClient
from telethon.sessions import StringSession


def order_data(data: list):
    # Associate each image with its song file
    zip_file = None
    music_file = None
    image_with_file_dict = {}
    for message in data:
        file_type = message.file.ext
        if file_type == '.jpg' and zip_file or music_file:
            image_with_file_dict[message.id] = [message, zip_file if zip_file is not None else music_file]
            zip_file = None
            music_file = None
        if file_type == '.mp3' and not zip_file:
            music_file = message
        if file_type in ['.zip', '.rar']:
            zip_file = message
    return image_with_file_dict


async def connect_telegram(channel_id: int):
    # get a list with all new files
    async with TelegramClient(StringSession(my_conf['string_auth']), my_conf['api_id'], my_conf['api_hash']) as client:
        entity = await client.get_entity(channel_id)
        # filter only the files from yester day into a list
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        daily_message = []
        async for message in client.iter_messages(entity):
            if message.date.date() == yesterday and message.file:
                daily_message.append(message)
            elif message.date.date() < yesterday:
                break

        # order the data and return
        music_with_image = order_data(daily_message)
        return music_with_image
