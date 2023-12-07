import telethon.tl.patched
from telethon import TelegramClient
from configuration import my_conf
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from telethon.sessions import StringSession


async def download_song(telegram_message: telethon.tl.patched.Message):
    # download file from Telegram and return his path
    client = TelegramClient(StringSession(my_conf['string_auth']), my_conf['api_id'], my_conf['api_hash'])
    await client.connect()
    file_name = os.path.join('temp', telegram_message.file.name)
    file_path = await client.download_media(telegram_message, file=file_name)
    client.disconnect()
    return file_path


def create_folder(folder_name: str):
    credentials = service_account.Credentials.from_service_account_file(
        my_conf['credentials_drive_path'],
        scopes=['https://www.googleapis.com/auth/drive']
    )

    # Build the Drive API client
    service = build('drive', 'v3', credentials=credentials)

    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }

    folder_id = folder.get('id')
    # Insert the permission for the folder
    service.permissions().create(
        fileId=folder_id,
        body=permission,
        fields='id'  # You can specify the fields you want to retrieve
    ).execute()
    return folder_id


def upload_song(file_path: str, file_type: str, folder_id: str):
    # Load the credentials from the JSON key file
    credentials = service_account.Credentials.from_service_account_file(
        my_conf['credentials_drive_path'],
        scopes=['https://www.googleapis.com/auth/drive']
    )

    # Build the Drive API client
    drive_service = build('drive', 'v3', credentials=credentials)

    # Create a media upload object
    media = MediaFileUpload(file_path, mimetype=file_type, resumable=True)

    # Set permissions for the file
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }

    # Upload the file to Google Drive
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    # Upload the file to Google Drive
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    )

    response = None
    while response is None:
        status, response = file.next_chunk()

    # close the file to delete it
    media.stream().close()

    drive_service.permissions().create(
        fileId=response['id'],
        body=permission
    ).execute()

    # delete the file after upload
    os.remove(file_path)

    file_id = response['id']

    file_link = f"https://drive.google.com/file/d/{file_id}/view"

    return file_link


async def telegram_to_drive(telegram_message: telethon.tl.patched.Message, folder_id: str):
    # do the all processes: download & upload return the link
    file_path = await download_song(telegram_message)
    file_link = upload_song(file_path, telegram_message.file.mime_type, folder_id)
    return file_link, (os.path.basename(file_path).split('.')[0] + ';').replace('_', ' ')
