from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

questions_collection = db["questions"]

# Optional: clear previous questions
questions_collection.delete_many({})

questions = [

{
"question": "Solve: 2x + 4 = 10",
"options": ["2", "3", "4", "5"],
"correct_answer": "3",
"difficulty": 0.2,
"topic": "Algebra",
"tags": ["linear equation"]
},

{
"question": "Solve: 3x = 21",
"options": ["5", "6", "7", "8"],
"correct_answer": "7",
"difficulty": 0.25,
"topic": "Algebra",
"tags": ["basic algebra"]
},

{
"question": "Solve: 2x + 3 = 11",
"options": ["2", "3", "4", "5"],
"correct_answer": "4",
"difficulty": 0.45,
"topic": "Algebra",
"tags": ["linear equation"]
},

{
"question": "Solve: 4x − 5 = 11",
"options": ["3", "4", "5", "6"],
"correct_answer": "4",
"difficulty": 0.6,
"topic": "Algebra",
"tags": ["equations"]
},

{
"question": "Solve: 5x + 10 = 35",
"options": ["3", "4", "5", "6"],
"correct_answer": "5",
"difficulty": 0.75,
"topic": "Algebra",
"tags": ["multi-step"]
},

{
"question": "What is 5 × 6?",
"options": ["20", "25", "30", "35"],
"correct_answer": "30",
"difficulty": 0.1,
"topic": "Arithmetic",
"tags": ["multiplication"]
},

{
"question": "What is 12% of 100?",
"options": ["10", "12", "14", "15"],
"correct_answer": "12",
"difficulty": 0.5,
"topic": "Arithmetic",
"tags": ["percentage"]
},

{
"question": "What is 15²?",
"options": ["200", "215", "225", "250"],
"correct_answer": "225",
"difficulty": 0.8,
"topic": "Arithmetic",
"tags": ["squares"]
},

{
"question": "Area of a square with side 5?",
"options": ["20", "25", "30", "15"],
"correct_answer": "25",
"difficulty": 0.35,
"topic": "Geometry",
"tags": ["area"]
},

{
"question": "Perimeter of rectangle 4x6?",
"options": ["20", "24", "18", "22"],
"correct_answer": "20",
"difficulty": 0.4,
"topic": "Geometry",
"tags": ["perimeter"]
},

{
"question": "Volume of cube with side 3?",
"options": ["9", "18", "27", "36"],
"correct_answer": "27",
"difficulty": 0.65,
"topic": "Geometry",
"tags": ["volume"]
},

{
"question": "Diagonal of square with side 4?",
"options": ["4", "5.6", "6", "8"],
"correct_answer": "5.6",
"difficulty": 0.85,
"topic": "Geometry",
"tags": ["diagonal"]
},

{
"question": "Synonym of 'Rapid'",
"options": ["Slow", "Fast", "Weak", "Soft"],
"correct_answer": "Fast",
"difficulty": 0.55,
"topic": "Vocabulary",
"tags": ["verbal"]
},

{
"question": "Antonym of 'Expand'",
"options": ["Grow", "Spread", "Shrink", "Stretch"],
"correct_answer": "Shrink",
"difficulty": 0.7,
"topic": "Vocabulary",
"tags": ["verbal"]
},

{
"question": "Meaning of 'Obscure'",
"options": ["Clear", "Hidden", "Bright", "Loud"],
"correct_answer": "Hidden",
"difficulty": 0.9,
"topic": "Vocabulary",
"tags": ["advanced"]
},

{
"question": "Synonym of 'Ancient'",
"options": ["Modern", "Old", "Future", "Young"],
"correct_answer": "Old",
"difficulty": 0.6,
"topic": "Vocabulary",
"tags": ["verbal"]
},

{
"question": "What is 8 × 7?",
"options": ["54", "56", "64", "58"],
"correct_answer": "56",
"difficulty": 0.3,
"topic": "Arithmetic",
"tags": ["multiplication"]
},

{
"question": "Solve: x/4 = 5",
"options": ["10", "15", "20", "25"],
"correct_answer": "20",
"difficulty": 0.5,
"topic": "Algebra",
"tags": ["equations"]
},

{
"question": "Area of rectangle 7x3?",
"options": ["20", "21", "24", "28"],
"correct_answer": "21",
"difficulty": 0.35,
"topic": "Geometry",
"tags": ["area"]
},

{
"question": "Meaning of 'Benevolent'",
"options": ["Kind", "Angry", "Weak", "Cold"],
"correct_answer": "Kind",
"difficulty": 0.85,
"topic": "Vocabulary",
"tags": ["advanced"]
}

]

# Insert into MongoDB
questions_collection.insert_many(questions)

print(f"Seeded {len(questions)} questions successfully!")