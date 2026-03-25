
import os
import uuid
import aiofiles
from aiogram import Bot
from aiogram.types import PhotoSize, Voice, Document, VideoNote

PHOTOS_DIR = "media/photos"
VOICES_DIR = "media/voices"
DOCUMENTS_DIR = "media/documents"
VIDEO_NOTES_DIR = "media/video_notes"

os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(VOICES_DIR, exist_ok=True)
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(VIDEO_NOTES_DIR, exist_ok=True)


class FileService:

    @staticmethod
    async def download_photo(bot: Bot, photo: PhotoSize, user_id: int) -> str | None:
        try:
            file = await bot.get_file(photo.file_id)
            ext = file.file_path.rsplit(".", 1)[-1] if "." in file.file_path else "jpg"
            filename = f"{user_id}_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(PHOTOS_DIR, filename)

            file_bytes = await bot.download_file(file.file_path)

            async with aiofiles.open(filepath, "wb") as f:
                await f.write(file_bytes.read())

            return filepath

        except Exception as e:
            print(f"[FileService] download_photo failed: {e}")
            return None

    @staticmethod
    async def download_voice(bot: Bot, voice: Voice, user_id: int, language: str) -> str | None:
        try:
            file = await bot.get_file(voice.file_id)
            ext = file.file_path.rsplit(".", 1)[-1] if "." in file.file_path else "ogg"
            filename = f"{user_id}_{language}_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(VOICES_DIR, filename)

            file_bytes = await bot.download_file(file.file_path)

            async with aiofiles.open(filepath, "wb") as f:
                await f.write(file_bytes.read())

            return filepath

        except Exception as e:
            print(f"[FileService] download_voice failed: {e}")
            return None

    @staticmethod
    async def download_video_note(bot: Bot, video_note: VideoNote, user_id: int) -> str | None:
        try:
            file = await bot.get_file(video_note.file_id)
            ext = file.file_path.rsplit(".", 1)[-1] if "." in file.file_path else "mp4"
            filename = f"{user_id}_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(VIDEO_NOTES_DIR, filename)

            file_bytes = await bot.download_file(file.file_path)

            async with aiofiles.open(filepath, "wb") as f:
                await f.write(file_bytes.read())

            return filepath

        except Exception as e:
            print(f"[FileService] download_video_note failed: {e}")
            return None

    @staticmethod
    async def download_document(bot: Bot, doc: Document, user_id: int) -> str | None:
        try:
            file = await bot.get_file(doc.file_id)
            ext = doc.file_name.rsplit(".", 1)[-1] if doc.file_name and "." in doc.file_name else "pdf"
            filename = f"{user_id}_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(DOCUMENTS_DIR, filename)

            file_bytes = await bot.download_file(file.file_path)

            async with aiofiles.open(filepath, "wb") as f:
                await f.write(file_bytes.read())

            return filepath

        except Exception as e:
            print(f"[FileService] download_document failed: {e}")
            return None

    @staticmethod
    def delete_file(filepath: str) -> None:
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"[FileService] delete_file failed: {e}")