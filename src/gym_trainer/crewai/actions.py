import nanoid

from gym_trainer.crewai.agents import crew

def start_session():
    session_id = nanoid.generate(size=5)
    # TODO: Create session in database
    return session_id

def answer(input_prompt):
    try:
        response = crew.kickoff({
            "user_data": input_prompt
        })
        return response.raw
    except ValueError as e:
        print(str(e))
        return ""