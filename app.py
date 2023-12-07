import asyncio
from get_songs_from_telegram import connect_telegram
from send_design_mail import send_mail
from from_telegram_to_gdrive import telegram_to_drive, create_folder
from create_image_html import create_image_box
from create_designed_html_email import create_html
from configuration import my_conf
from datetime import datetime
import sys


def set_mode():
    try:
        args = sys.argv[1:]
        channel_mode = args[0]
    except IndexError:
        raise ValueError("No arguments provided. Please provide at least one argument.")
    if channel_mode == 'israeli':
        channel_id = my_conf['music_channel_id']
        title = 'שירים חדשים - ישראלי'
        description = 'IL_MUSIC_'
    elif channel_mode == 'dos':
        channel_id = my_conf['dos_channel_id']
        title = 'שירים חדשים - חרדי'
        description = 'DOS_MUSIC_'
    else:
        raise ValueError("No valid arguments provided. Please provide valid args")
    return channel_id, title, description


async def main():
    channel_id, title, description = set_mode()

    # create dict with songs and image
    new_songs_dict = await connect_telegram(channel_id)
    print(len(new_songs_dict))

    # if there is no new songs stop the script
    if len(new_songs_dict) < 1:
        exit()

    # create an image box with html template for each song
    all_image_boxes = []

    # defined parent folder for all daily content
    daily_folder = description + str(datetime.now().date())
    folder_id = create_folder(daily_folder)
    folder_link = f'https://drive.google.com/drive/folders/{folder_id}'
    for image_message, song_message in new_songs_dict.values():
        # download the file from telegram and upload it to google-drive
        file_link, file_name = await telegram_to_drive(song_message, folder_id)
        all_image_boxes.append(await create_image_box(image_message, file_link, file_name))

    # create the full html message from all song boxes
    data_to_table = [image_box['image_box'] for image_box in all_image_boxes]
    html_message = create_html(data_to_table, folder_link)

    # add the image objects into the mail and send it for all members
    image_objects = [image_box['image_object'] for image_box in all_image_boxes]
    send_mail(title, html_message, image_objects)


if __name__ == '__main__':
    print(f'start run at: {datetime.now()}')
    # execute the script in event loop because its async code
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
