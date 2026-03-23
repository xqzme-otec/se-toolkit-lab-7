async def handle_help() -> str:
    return """📋 Available commands:

/start - Welcome message
/help - Show this help
/health - Check backend status
/labs - List all available labs
/scores <lab> - Show pass rates for a lab

💡 You can also ask questions in plain language, like:
- "What labs are available?"
- "Show me scores for lab-04"
- "Is the system healthy?" """