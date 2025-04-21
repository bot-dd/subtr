user_lang = {}

def set_user_lang(user_id, lang_code):
    user_lang[user_id] = lang_code

def get_user_lang(user_id):
    return user_lang.get(user_id, "bn")  # Default Bangla
