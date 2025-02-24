from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
import json
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.comment import Comment
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

# todo:
#Add delete button
# user fills out forms whose inputs are the leaves of a tree!




# Load plant data from JSON
def load_plants():
    with open('flask_app/json/plants.json', 'r') as file:
        return json.load(file)
    

@app.route("/")
def index():
    # session.pop("user_id")
    if not "user_id" in session:
        return render_template("index.html")
    else:
        return redirect(f"/profile/{session["user_id"]}")

@app.route('/registering', methods=['POST'])
def registering():
    # validating the form
    # If there's errors
    if not User.validate_form(request.form):
        session["fname"] = request.form["fname"]
        session["lname"] = request.form["lname"]
        session["email"] = request.form["email"]
        return redirect('/')
    if not User.validate_email(request.form):
        session["fname"] = request.form["fname"]
        session["lname"] = request.form["lname"]
        session["email"] = request.form["email"]
        return redirect('/')
    if User.same_email(request.form):
        session["fname"] = request.form["fname"]
        session["lname"] = request.form["lname"]
        session["email"] = request.form["email"]
        return redirect('/')
    print("user form validated")
    #If there's no errors:
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    print("Creating hash:", pw_hash)
    # put the pw_hash into the data dictionary
    data = {
    "first_name": request.form['fname'],
    "last_name": request.form['lname'],
    "email": request.form['email'],
    "password": pw_hash
    }
    print("data created")
    # Call the save @classmethod on User
    user_id = User.save(data)
    print("user saved")
    # store user id into session
    session['user_id'] = user_id
    # Don't forget to redirect after saving to the database.
    session.pop('email', None)
    session.pop('fname', None)
    session.pop('lname', None)
    return redirect(f'/profile/{session['user_id']}')

@app.route("/logging_in", methods=["POST"])
def logging_in():
    # see if the username provided exists in the database
    data = { "email" : request.form["login_email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", category="box2")
        session["login_email"] = request.form["login_email"]
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", category="box2")
        session["login_email"] = request.form["login_email"]
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session.pop('login_email', None)
    # never render on a post!!!
    return redirect(f"/profile/{session['user_id']}")


@app.route("/profile/<int:id>")
def dashboard(id):
    if not 'user_id' in session:
        return redirect("/")
    else:
        session.pop('fname', None)
        session.pop('lname', None)
        session.pop("email", None)
        user= User.get_one(session['user_id'])
        # Profile variable is the profile's user info which may or may not be the same as the logged-in user.
        profile= User.get_one(id)
        return render_template("profile.html", user=user, profile=profile)

@app.route("/profile/edit/<int:id>", methods=["get"])
def edit_profile(id):
    if not 'user_id' in session:
        return redirect("/")
    else:
        user= User.get_one(session['user_id'])
        profile= User.get_one(id)
        return render_template("profile_edit.html", user=user, profile=profile)

@app.route("/profile/editing/<int:id>", methods=["post"])
def editing_profile(id):
    if not 'user_id' in session:
        return redirect("/")
    else:
        data = {
            "bio": request.form["bio"],
            "user_id": session["user_id"]
            }
        User.edit_bio(data)
        return redirect(f"/profile/{session["user_id"]}")


@app.route("/learn")
def learn():
    if not "user_id" in session:
        return redirect("/")
    user= User.get_one(session['user_id'])
    return render_template("learn.html", user=user)

@app.route("/quizzes")
def quizzes():
    if not "user_id" in session:
        return redirect("/")
    user= User.get_one(session['user_id'])
    return render_template("quizzes.html", user=user)

@app.route("/forum")
def form():
    if not "user_id" in session:
        return redirect("/")
    user= User.get_one(session['user_id'])
    all_posts = Post.get_all_posts()
    all_comments = Comment.get_all()
    return render_template("forum.html", user=user, all_posts=all_posts, all_comments = all_comments)

@app.route("/posting", methods=["POST"])
def posting():
    print("Entered posting route")
    if not Post.validate_post(request.form):
        print("Post not validated!")
        session["title"] = request.form['title']
        session["content"] = request.form['content']
        return redirect ("/form")
    print("Post validated")
    data = {
        "title": request.form['title'],
        "content": request.form['content'],
        "user_id": session['user_id'],
    }
    print("Data created.")
    Post.save_post(data)
    return redirect("/forum")


@app.route("/commenting/<int:post_id>", methods=["POST"])
def commenting(post_id):
    print("Entered commenting route")
    if not Comment.validate(request.form):
        print("Comment not validated!")
        session["content"] = request.form['content']
        return redirect ("/forum")
    print("Post validated")
    data = {
        "content": request.form["comment"],
        "post_id": post_id,
        "user_id": session['user_id'],
    }
    print("Data created.")
    Comment.save_comment(data)
    return redirect("/forum")

@app.route("/restart_quiz/<quiz_type>")
def restart(quiz_type):
    session.pop("current_question", None)
    session.pop("score", None)
    return redirect(f"/quiz_{quiz_type}")

@app.route("/quiz_Herb", methods=['GET', 'POST'])
def herb():
    if not "user_id" in session:
        return render_template("index.html")
    else:
        # session.pop("current_question", None)
        # session.pop("score", None)
        plants = load_plants()
        print("plants:", plants["quizzes"][0]["questions"])
    # Ensure current_question exists in the session, default to 0 if not
    if not "current_question" in session:
        session["current_question"] = 0
    if not "score" in session:    
        session["score"] = 0

    current_question = session['current_question']
    total = len(plants["quizzes"][0]["questions"])
    user= User.get_one(session['user_id'])
    
    # If there are no more questions, show the result
    if current_question >= len(plants["quizzes"][0]["questions"]):
        score= session["score"]
        data={"herb": score, "user_id": session["user_id"]}
        User.edit_herb(data)
        session.pop("current_question", None)
        session.pop("score", None)
        return render_template('result.html', total=total, user=user, score=score)
    
    quiz_type= plants["quizzes"][0]["name"]
    plant = plants["quizzes"][0]["questions"][current_question]
    print("plant:", plant)
    print("Go until", len(plants["quizzes"][0]["questions"]))

    if request.method == 'POST':
        print("Method is post!")
        # Check the answer
        selected_answer = request.form.get('answer')
        correct_answer = plant['answer']
        
        # Update score if the answer is correct
        if selected_answer == correct_answer:
            print("Score up!")
            session['score'] += 1
        
        # Move to the next question
        session['current_question'] = current_question + 1
        flash('Correct!' if selected_answer == correct_answer else 'Incorrect!')

        return redirect("/quiz_Herb")

    return render_template('quiz.html', plant=plant, question_number=current_question + 1, user=user, quiz_type=quiz_type, total=total)


@app.route("/quiz_Flower", methods=['GET', 'POST'])
def flower():
    if not "user_id" in session:
        return render_template("index.html")
    else:
        # session.pop("current_question", None)
        # session.pop("score", None)
        plants = load_plants()
        print("plants:", plants["quizzes"][1]["questions"])
    # Ensure current_question exists in the session, default to 0 if not
    if not "current_question" in session:
        session["current_question"] = 0
    if not "score" in session:    
        session["score"] = 0

    # Important info for HTML
    current_question = session['current_question']
    user= User.get_one(session['user_id'])
    total = len(plants["quizzes"][1]["questions"])
    quiz_type= plants["quizzes"][1]["name"]
    
    print("Current Q:", current_question)

    # If there are no more questions, show the result
    if current_question >= len(plants["quizzes"][1]["questions"]):
        score= session["score"]
        new_score={"flower": score, "user_id": session["user_id"]}
        User.edit_herb(new_score)
        session.pop("current_question", None)
        session.pop("score", None)
        
        return render_template('result.html',  user=user, score=score, total=total, quiz_type=quiz_type)
    
    
    plant = plants["quizzes"][1]["questions"][current_question]
    print("plant:", plant)
    print("Go until", len(plants["quizzes"][1]["questions"]))

    if request.method == 'POST':
        print("Method is post!")
        # Check the answer
        selected_answer = request.form.get('answer')
        correct_answer = plant['answer']
        
        # Update score if the answer is correct
        if selected_answer == correct_answer:
            print("Score up!")
            session['score'] += 1
        
        # Move to the next question
        session['current_question'] = current_question + 1
        flash('Correct!' if selected_answer == correct_answer else 'Incorrect!')

        return redirect("/quiz_Flower")

    return render_template('quiz.html', plant=plant, question_number=current_question + 1, user=user, total=total, quiz_type=quiz_type)



# @app.route("/edit/<int:post>")
# def edit_post(post):
#     sighting = Sighting.get_one(post)
#     user= User.get_one(session['user_id'])
#     return render_template("edit.html", sighting=sighting, user=user)

# @app.route("/editing", methods=["POST"])
# def editing_post():
#     if not Sighting.validate_post(request.form):
#         print("Post not validated!")
#         session["location"] = request.form['location']
#         session["date"] = request.form['date']
#         session["number_of_sasquatches"] = request.form['number_of_sasquatches']
#         session["details"] = request.form['details']
#         return redirect (f"/edit/{request.form['sighting_id']}")
#     print("Post validated")
#     Sighting.edit(request.form)
#     session.pop('location', None)
#     session.pop('date', None)
#     session.pop("number_of_sasquatches", None)
#     session.pop("details", None)
#     return redirect(f"/sightings/show/{request.form['sighting_id']}")


@app.route("/deleting/<int:post>")
def deleting_post(post):
    Post.delete_post(post)
    return redirect("/dashboard")


@app.route("/logging_out")
def logging_out():
    session.pop('user_id', None)
    return redirect("/")
