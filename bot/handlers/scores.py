async def handle_scores(lab: str = None) -> str:
    if not lab:
        return "Usage: /scores <lab-name>\nExample: /scores lab-01"
    return f"📊 Scores for {lab} - coming soon"
