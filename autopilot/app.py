"""
AUTOPILOT main application.

- Loads config via autopilot.config
- Creates a Pyrogram Client
- Registers handlers (/start, /dev, /ping)
- Robust logging and graceful failure on missing config
"""

import asyncio
import logging
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .config import load_config

LOG_FORMAT = "%(asctime)s | %(levelname)-5s | %(name)s | %(message)s"

DEV_CAPTION = (
    "YOUSEF SHAHEEN | Coding the future, beyond the limits of imagination.\n\n"
    "أنا لا أبني مجرد بوتات تليجرام، بل أصيغ حلولاً رقمية ذكية تتنفس الابتكار. "
    "Engineering excellence بلمسة فنية، لنحول أفكارك إلى واقع automated يسبق زمنه.\n\n"
    "Ready to disrupt? Let's connect: 📩 @Y9_S4"
)

DEV_IMAGE = "https://i.postimg.cc/tgrqP2sW/IMG-20260620-133210-543.jpg"

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, stream=sys.stdout)
    # Reduce verbosity of noisy libs
    logging.getLogger("pyrogram").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def create_client(cfg):
    """
    Create a Pyrogram Client for the Bot API via bot_token.
    Session name is ephemeral ("autopilot").
    """
    return Client(
        "autopilot",
        bot_token=cfg.TOKEN,
    )

def build_dev_keyboard():
    """
    6 buttons:
     1. Instagram
     2. Telegram (username)
     3. TikTok
     4. Facebook
     5. WhatsApp
     6. Support (telegram)
    """
    buttons = [
        [
            InlineKeyboardButton("Instagram", url="https://www.instagram.com/1.0_v_?igsh=N2N5MXNwN3p4ZDY2"),
            InlineKeyboardButton("Telegram", url="https://t.me/Y9_S4"),
        ],
        [
            InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@zix8ii?_r=1&_d=f3c01a6371bii9&sec_uid="),
            InlineKeyboardButton("Facebook", url="https://www.facebook.com/share/1BkTUUih6e/"),
        ],
        [
            InlineKeyboardButton("WhatsApp", url="https://wa.link/lc6f5w"),
            InlineKeyboardButton("Support", url="https://t.me/shaheen_ys"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

async def main():
    setup_logging()
    logger = logging.getLogger("autopilot")
    logger.info("Loading configuration")
    try:
        cfg = load_config()
    except Exception as exc:
        logger.exception("Configuration error: %s", exc)
        # Fail early with a non-zero exit via exception
        raise

    app = create_client(cfg)

    # Register handlers
    @app.on_message(filters.command(["start", "dev"]) & filters.private)
    async def start_dev_handler(client: Client, message: Message):
        """
        Sends developer profile image, caption and inline keyboard.
        If sending photo fails, falls back to plain text reply.
        """
        try:
            keyboard = build_dev_keyboard()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=DEV_IMAGE,
                caption=DEV_CAPTION,
                reply_markup=keyboard,
            )
        except Exception:
            logger.exception("Failed to send dev/start message")
            # fallback to simple text reply
            try:
                await message.reply_text(DEV_CAPTION)
            except Exception:
                logger.exception("Fallback reply also failed")

    @app.on_message(filters.command("ping") & filters.private)
    async def ping_handler(client: Client, message: Message):
        try:
            await message.reply_text("pong")
        except Exception:
            logger.exception("Failed to reply to ping")

    # Start client
    logger.info("Starting Pyrogram client")
    try:
        await app.start()
    except Exception:
        logger.exception("Failed to start Pyrogram client")
        raise

    logger.info("AUTOPILOT started successfully")
    # Keep running until a cancellation (SIGTERM) occurs
    stop_event = asyncio.Event()
    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        logger.info("Shutdown requested: cancelled")
    finally:
        logger.info("Stopping Pyrogram client")
        await app.stop()
