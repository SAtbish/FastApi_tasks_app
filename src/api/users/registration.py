from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status


@router.post("/registration")
async def user_registration_handler():
    return JSONResponse(content={"user": "registered"}, status_code=status.HTTP_200_OK)
