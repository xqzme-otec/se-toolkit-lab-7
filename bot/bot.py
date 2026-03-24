#!/usr/bin/env python3
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from handlers.start import handle_start
from handlers.help import handle_help
from handlers.health import handle_health
from handlers.labs import handle_labs
from handlers.scores import handle_scores


async def process_command(command: str) -> str:
    command = command.strip()
    
    if command == "/start":
        return await handle_start()
    elif command == "/help":
        return await handle_help()
    elif command == "/health":
        return await handle_health()
    elif command == "/labs":
        return await handle_labs()
    elif command.startswith("/scores"):
        parts = command.split()
        lab = parts[1] if len(parts) > 1 else None
        return await handle_scores(lab)
    else:
        return f"Unknown command: {command}\nUse /help to see available commands."


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Test a command")
    args = parser.parse_args()
    
    if args.test:
        response = await process_command(args.test)
        print(response)
        sys.exit(0)
    else:
        from aiogram import Bot, Dispatcher
        from aiogram.types import Message
        from config import BOT_TOKEN
        
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        
        @dp.message()
        async def handle_message(message: Message):
            response = await process_command(message.text)
            await message.answer(response)
        
        async def start_bot():
            print("Bot started!")
            await dp.start_polling(bot)
        
        await start_bot()


if __name__ == "__main__":
    asyncio.run(main())