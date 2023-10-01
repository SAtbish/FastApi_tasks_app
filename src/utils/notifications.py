import hashlib

from src.schemas.notifications import NotificationRedisModel

confirm_email_header = "Please confirm your email."
confirm_email_message = lambda email, user_id: f'<div><h1 style="color: red;">Здравствуйте, Click here: http://127.0.0.1:8000/users/confirm/email/{user_id}/{hashlib.md5(bytes(email, "utf-8")).hexdigest()}</h1></div>'


def make_confirm_email_notification(email: str, user_id: int) -> NotificationRedisModel:
    return NotificationRedisModel(
        header=confirm_email_header,
        message=confirm_email_message(email, user_id),
        type="confirm_email",
        user_id=user_id
    )


