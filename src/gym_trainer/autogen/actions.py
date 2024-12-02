import nanoid

def start_session():
    session_id = nanoid.generate(size=5)
    # TODO: Create session in database
    return session_id
