from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import sessions_collection, questions_collection
from app.services.adaptive_engine import get_next_question
from app.utils.irt import update_ability
from app.models.request_models import AnswerSubmission
from app.services.ai_plan import generate_study_plan

import uuid

router = APIRouter()


@router.post("/start-session")
def start_session():

    session_id = str(uuid.uuid4())

    session = {
        "_id": session_id,
        "ability_score": 0.5,
        "questions_answered": [],
        "completed": False
    }

    sessions_collection.insert_one(session)

    return {
        "session_id": session_id,
        "ability": 0.5
    }


@router.get("/next-question/{session_id}")
def next_question(session_id: str):

    session = sessions_collection.find_one({"_id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    ability = session["ability_score"]

    asked = [
        ObjectId(q["question_id"])
        for q in session["questions_answered"]
    ]

    question = get_next_question(ability, asked)

    if not question:
        return {"message": "No more questions"}

    return {
        "question_id": str(question["_id"]),
        "question": question["question"],
        "options": question["options"],
        "difficulty": question["difficulty"]
    }


@router.post("/submit-answer")
def submit_answer(data: AnswerSubmission):

    session = sessions_collection.find_one({"_id": data.session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    question = questions_collection.find_one(
        {"_id": ObjectId(data.question_id)}
    )

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    correct = data.answer == question["correct_answer"]

    ability = session["ability_score"]

    new_ability = update_ability(
        ability,
        question["difficulty"],
        correct
    )

    sessions_collection.update_one(
        {"_id": data.session_id},
        {
            "$push": {
                "questions_answered": {
                    "question_id": data.question_id,
                    "correct": correct,
                    "difficulty": question["difficulty"],
                    "topic": question["topic"]
                }
            },
            "$set": {
                "ability_score": new_ability,
                "completed": len(session.get("questions_answered", [])) + 1 >= 10
            }
        }
    )

    return {
        "correct": correct,
        "new_ability": new_ability
    }


@router.get("/study-plan/{session_id}")
def study_plan(session_id: str):
    session = sessions_collection.find_one({"_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if not session.get("completed", False):
        raise HTTPException(status_code=400, detail="Session not completed yet")
        
    study_plan_text = generate_study_plan(session)
    
    return {
        "session_id": session_id,
        "ability_score": session.get("ability_score"),
        "study_plan": study_plan_text
    }