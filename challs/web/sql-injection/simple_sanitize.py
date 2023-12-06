def sanitize_input(key):
    blocked_words = ['INSERT', 'UPDATE', 'UNION', ';', '--', '/', ' ']

    for word in blocked_words:
        if word in key.upper():
            return None

    return key
    # If no blocked words are found, return the sanitized input
    return True
