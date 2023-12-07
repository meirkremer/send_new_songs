from email.mime.image import MIMEImage
import telethon.tl.patched
from configuration import my_conf
from telethon import TelegramClient
from jinja2 import Template
from telethon.sessions import StringSession


async def connect_telegram(image_message: telethon.tl.patched.Message):
    # connect to telegram and download the image into variable
    async with TelegramClient(StringSession(my_conf['string_auth']), my_conf['api_id'], my_conf['api_hash']) as client:
        blob_image = await client.download_media(image_message, bytes)
        return blob_image


async def create_image_box(image_message: telethon.tl.patched.Message, file_link: str, file_name: str):
    # get the image from Telegram
    blob_image = await connect_telegram(image_message)
    image_id = str(image_message.id) + 'jpg'

    # create an image object for the mail
    img = MIMEImage(blob_image, name=image_id)
    img.add_header('Content-ID', f'<{image_id}>')

    # create a box for the song with image and link
    with open('templates/truck.html', 'r', encoding='utf-8') as f:
        box_template = Template(f.read())

    image_box = box_template.render(song_link=file_link, song_image=f'cid:{image_id}',
                                    song_name=f'"{file_name}"', song_title=file_name.replace(';', ''))
    return {'image_object': img, 'image_box': image_box}
