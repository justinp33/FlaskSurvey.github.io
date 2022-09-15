from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    """Shows user title of survey, instructions, and provides a button to start the survey."""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions

    return render_template("startpage.html", title = title, instructions = instructions, questions = questions)

@app.route('/questions/<int:question_num>')
def show_question(question_num):
    """Show question to user"""

    question = satisfaction_survey.questions[question_num].question
    choices = satisfaction_survey.questions[question_num].choices

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
    
    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != question_num):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {question_num}.")
        return redirect(f"/questions/{len(responses)}")

    return render_template(
        "questions.html", question=question, choices=choices)
    
@app.route('/answer', methods = ["POST"])
def answer_question():

    response = request.form["answer"]
    responses.append(response)

    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def complete():
    """Let user know they have completed the survey."""

    return render_template("completion.html")