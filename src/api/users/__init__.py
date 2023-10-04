from src.api.users.registration import router
from src.api.users.login import router
from src.api.users.get_all import router
from src.api.users.get_all_paginated import router
from src.api.users.get import router
from src.api.users.delete import router
from src.api.users.update_info import router
from src.api.users.update_password import router
from src.api.users.confirm_email import router


__all__ = ["router"]
