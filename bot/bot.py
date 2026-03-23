#!/usr/bin/env python3
import argparse
import asyncio
import sys
from pathlib import Path

# Добавляем bot в путь
sys.path.insert(0, str(Path(__file__).parent))

from handlers.start import handle_start
from handlers.help import handle_help
from handlers.health import handle_health


async def process_command(command: str) -> str:
    """Обрабатывает команду и возвращает ответ."""
    
    # Убираем лишние пробелы
    command = command.strip()
    
    if command == "/start":
        return await handle_start()
    elif command == "/help":
        return await handle_help()
    elif command == "/health":
        return await handle_health()
    elif command == "/labs":
        # Пока заглушка
        return "📚 Labs list - coming soon"
    elif command.startswith("/scores"):
        # Пока заглушка
        return "📊 Scores - coming soon"
    else:
        return f"Unknown command: {command}\nUse /help to see available commands."


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Test a command and print response")
    args = parser.parse_args()
    
    if args.test:
        try:
            response = await process_command(args.test)
            print(response)
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Bot running in Telegram mode - coming soon")


if __name__ == "__main__":
    asyncio.run(main())