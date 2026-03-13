import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import Response
from dotenv import load_dotenv

from core.config import config
from core.logging import setup_logging
from database.database import init_db
from bot.handlers import register_handlers
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.anti_spam import AntiSpamMiddleware
from bot.middlewares.private_chat_only import PrivateChatOnlyMiddleware

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

WEBHOOK_PATH = "/webhook/bot"
WEBHOOK_SECRET = "mysecrettoken"

bot = Bot(token=config.bot_token)
dp = Dispatcher()


def setup_middlewares():
    dp.message.middleware(ThrottlingMiddleware(
        calls=1,
        per=1,
        warning_message="⏳ Iltimos, sekinroq yozing!"
    ))
    dp.message.middleware(PrivateChatOnlyMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.message.middleware(AntiSpamMiddleware())
    dp.callback_query.middleware(AuthMiddleware())


async def on_startup():
    await init_db()
    logger.info("Database initialized")
    setup_middlewares()
    register_handlers(dp)
    logger.info("Handlers registered")


async def on_shutdown():
    await bot.session.close()
    logger.info("Bot stopped")


async def polling():
    await on_startup()
    logger.info("Bot started in polling mode")
    await dp.start_polling(bot)
    await on_shutdown()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    logger.info("Bot started in webhook mode")
    yield
    await on_shutdown()

app = FastAPI(lifespan=lifespan)

def create_app() -> FastAPI:
    @app.post(WEBHOOK_PATH)
    async def webhook(request: Request) -> Response:
        update = await request.json()
        await dp.feed_raw_update(bot, update)
        return Response()

    return app



@app.get("/health")
async def health_check():
    return {"status": "healthy", "status_code": status.HTTP_200_OK}

@app.get("/")
async def health() -> Response:
    return Response(status_code=200)


if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "polling"

    if mode == "webhook":
        uvicorn.run(
            "main:create_app",
            factory=True,
            host="0.0.0.0",
            port=8000,
            log_level="info",
        )
    else:
        try:
            asyncio.run(polling())
        except KeyboardInterrupt:
            pass