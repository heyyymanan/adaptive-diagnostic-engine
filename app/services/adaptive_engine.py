from app.database import questions_collection


def get_next_question(ability, asked_questions):

    questions = list(
        questions_collection.find(
            {"_id": {"$nin": asked_questions}}
        )
    )

    if not questions:
        return None

    questions.sort(
        key=lambda q: abs(q["difficulty"] - ability)
    )

    return questions[0]