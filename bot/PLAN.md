# LMS Telegram Bot - Development Plan

## Architecture
The bot uses a testable handler pattern where all command logic is separated from the Telegram transport layer. Handlers are async functions that take parameters and return text, making them testable via CLI with `--test` flag.

## P0 - Core Commands (Task 1-2)
- `/start`, `/help`, `/health`, `/labs`, `/scores` - basic slash commands
- Backend integration via HTTP client to fetch real data from LMS API
- Error handling for backend downtime

## P1 - Natural Language Routing (Task 3)
- LLM integration to interpret plain text queries
- All 9 backend endpoints exposed as LLM tools
- Intent routing: map user messages to appropriate API calls
- Multi-step reasoning for complex queries

## P2 - Enhanced UX
- Inline keyboards for common actions
- Rich formatting with tables
- Response caching for frequent queries
- Multi-turn conversation context

## P3 - Deployment
- Dockerfile for bot containerization
- Integration into existing docker-compose.yml
- Deployment to VM with proper environment variables
- Documentation in README

## Timeline
1. Scaffold and test mode ✅
2. Backend API client + slash commands
3. LLM tool integration
4. Containerization and deployment