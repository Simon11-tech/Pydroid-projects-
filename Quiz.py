import threading
import time

# Your questions
questions = [
    {
        "question": "What is the capital of Nigeria?",
        "options": ["A. Lagos", "B. Abuja", "C. Kano", "D. Benin"],
        "answer": "B"
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["A. Python", "B. Java", "C. HTML", "D. C++"],
        "answer": "C"
    },
    {
        "question": "What does CPU stand for?",
        "options": ["A. Central Process Unit", "B. Computer Personal Unit", "C. Central Processing Unit", "D. Control Processing Unit"],
        "answer": "C"
    }
]

score = 0
TIME_LIMIT = 10  # seconds per question
user_answer = None

def ask_with_timeout(prompt):
    global user_answer
    user_answer = None

    def get_input():
        global user_answer
        user_answer = input(prompt).strip().upper()

    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(TIME_LIMIT)

    if thread.is_alive():
        print(f"\n⏰ Time's up! Moving on...")
        return None
    return user_answer

print("\n🧠 Welcome to the Timed Quiz!\n")

for i, q in enumerate(questions, 1):
    print(f"Q{i}: {q['question']}")
    for opt in q["options"]:
        print(opt)

    ans = ask_with_timeout("Your answer (A/B/C/D): ")

    if ans is None:
        print(f"❌ No answer. Correct answer: {q['answer']}\n")
        continue

    if ans == q["answer"]:
        print("✅ Correct!\n")
        score += 1
    else:
        print(f"❌ Wrong! Correct answer is {q['answer']}\n")

print(f"🎉 Quiz Complete! Your score: {score}/{len(questions)}")