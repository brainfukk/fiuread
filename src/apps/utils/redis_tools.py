from hashlib import md5

from django.conf import settings

from src.configs.redisconf import get_connection


def __cast_bool(status: str):
    return status in ("True", "true", "1", 1, "yes")


def construct_email_token_register_key(username: str, user_email: str):
    key = "{username}:{user_email}:{user_email_hash}".format(
        username=username,
        user_email=user_email,
        user_email_hash=md5(user_email.encode()).hexdigest(),
    )
    return md5((key + settings.SECRET_KEY).encode()).hexdigest()


def set_email_token_confirmation(key: str, username: str, user_email: str) -> None:
    connection = get_connection()
    return connection.hset(
        name=key,
        mapping={"username": username, "user_email": user_email, "status": "False"},
    )


def check_user_token(username: str, user_email: str, key: str) -> bool:
    connection = get_connection()
    data = connection.hgetall(name=key)

    if data.get("username") is None:
        return False
    if data.get("user_email") is None:
        return False
    if username != data["username"]:
        return False
    if user_email.lower().strip() != data["user_email"].lower().strip():
        return False
    return True


def confirm_user_token(key: str):
    connection = get_connection()
    data = connection.hgetall(name=key)
    data["status"] = "True"
    connection.hset(name=key, mapping=data)


def check_user_confirmation_status(username: str, email: str):
    connection = get_connection()
    key = construct_email_token_register_key(username=username, user_email=email)
    data = connection.hgetall(key)
    return __cast_bool(data["status"])
