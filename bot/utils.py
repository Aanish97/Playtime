from bot.models import User, ChatMessage


def get_user(user_json: dict) -> User:
    """
        User Object: {
            'first_name': 'Aanish',
            'last_name': 'Amir',
            'profile_pic': 'https://platform-lookaside.fbsbx.com/platform/profilepic/?eai=AXFzbBNT7xDqR5J9qQj6JENsN3gEW0KD73kX1cpJaquo8d_8tO5pAb-ZZaSxHXagEGGg26CZuTlv&psid=7661864127265279&width=1024&ext=1721320807&hash=AbbICa2JQCQo4L5SwVkyIduB',
            'id': '7661864127265279'
        }

        return: User object
    """
    user_obj, created = User.objects.get_or_create(facebook_id=user_json.get('id'))

    if created:
        user_obj.first_name = user_json['first_name']
        user_obj.last_name = user_json['last_name']
        user_obj.profile_image = user_json['profile_pic']
        user_obj.save()

    return user_obj


def add_chat(message: str, response: str, user: User) -> None:
    ChatMessage.objects.create(
        message=message,
        bot_message=response,
        user=user
    )
