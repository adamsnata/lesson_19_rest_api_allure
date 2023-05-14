from voluptuous import Schema, PREVENT_EXTRA

user_schema = Schema(
    {
        "id": int,
        "email": str,
        "first_name": str,
        "last_name": str,
        "avatar": str,
    },
    extra=PREVENT_EXTRA,
    required=True
)

list_users_schema = Schema(
    {
        "page": int,
        "per_page": int,
        "total": int,
        "total_pages": int,
        "data": [user_schema],
        "support": {
            "url": str,
            "text": str
        }
    },
    extra=PREVENT_EXTRA,
    required=True
)


new_user_successful_register = Schema(
    {
        "id": int,
        "token": str,
    },
    extra=PREVENT_EXTRA,
    required=True
)

new_user_unsuccessful_register = Schema(
    {
        "error": str
    },
    extra=PREVENT_EXTRA,
    required=True
)

user_login_successful = Schema(
    {
        "token": str
    },
    extra=PREVENT_EXTRA,
    required=True
)

user_login_unsuccessful = Schema(
    {
        "token": str
    },
    extra=PREVENT_EXTRA,
    required=True
)
