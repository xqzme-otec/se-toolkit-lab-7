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
from services.lms_client import LMSClient
from services.llm_client import LLMClient
from services.tools import TOOLS, ToolExecutor
from config import LMS_API_BASE_URL, LMS_API_KEY, LLM_API_KEY, LLM_API_BASE_URL, LLM_API_MODEL

async def handle_natural_language(query: str) -> str:
    lms_client = LMSClient(LMS_API_BASE_URL, LMS_API_KEY)
    llm_client = LLMClient(LLM_API_KEY, LLM_API_BASE_URL, LLM_API_MODEL)
    tool_executor = ToolExecutor(lms_client)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant for a learning management system. You have access to tools that can fetch data about labs and scores. Use them to answer user questions."},
        {"role": "user", "content": query}
    ]
    
    max_iterations = 5
    for _ in range(max_iterations):
        response = await llm_client.chat(messages, tools=TOOLS)
        message = response["choices"][0]["message"]
        
        if not message.get("tool_calls"):
            return message.get("content", "I'm not sure how to answer that.")
        
        messages.append(message)
        
        for tool_call in message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            import json
            arguments = json.loads(tool_call["function"]["arguments"])
            print(f"[tool] LLM called: {tool_name}({arguments})", file=sys.stderr)
            
            result = await tool_executor.execute(tool_name, arguments)
            print(f"[tool] Result: {result[:100]}...", file=sys.stderr)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": result
            })
    
    return "I couldn't complete your request. Please try again."

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
    elif command.startswith("/"):
        return f"Unknown command: {command}\nUse /help to see available commands."
    else:
        return await handle_natural_language(command)

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
