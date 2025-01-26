@router.get("/health/detailed")
async def detailed_health():
    return {
        "database": await check_db_connection(),
        "cache": await check_cache_connection(),
        "background_tasks": await check_background_tasks(),
        "version": "1.0.0"
    } 