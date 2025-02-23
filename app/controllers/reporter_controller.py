from app.services.reporter_service import get_all_reporters

async def get_reporters():
    reporters = get_all_reporters()
    return {"reporters": reporters}