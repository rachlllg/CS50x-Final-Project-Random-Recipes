from cs50 import SQL
from django.shortcuts import render
from sqlalchemy import desc

from werkzeug.security import check_password_hash, generate_password_hash

from flask import Flask, flash, render_template, redirect, render_template_string, request, session
from flask_session import Session

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure recipe Library to use SQLite database
db = SQL("sqlite:///recipe.db")
# run sqlite3 in command line to execute SQLite commands
# run .open recipe.db to open the db file to see the tables
# create a new table 

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
  # if the user searched for recipe, show the users 10 recipes that match their search
  if request.method == "POST":
    recipe = request.form.get("recipe")
    recipe = recipe.lower()
    name = request.form.getlist("name")
    description = request.form.getlist("description")
    ingredients = request.form.getlist("ingredients")
    # if all three boxes are checked
    if not recipe:
      flash("please enter a search keyword")
      return redirect("/")
    elif name and description and ingredients:
      recipes = db.execute("SELECT * FROM recipe WHERE name LIKE ? OR description LIKE ? OR ingredients LIKE ? ORDER BY RANDOM() LIMIT 10", '%'+recipe+'%', '%'+recipe+'%', '%'+recipe+'%')
      return render_template("index.html", recipes=recipes)
    # if only one of the boxes is checked
    elif name and not description and not ingredients:
      recipes = db.execute("SELECT * FROM recipe WHERE name LIKE ? ORDER BY RANDOM() LIMIT 10", '%'+recipe+'%')
      return render_template("index.html", recipes=recipes)
    elif not name and description and not ingredients:
      recipes = db.execute("SELECT * FROM recipe WHERE description LIKE ? ORDER BY RANDOM() LIMIT 10", '%'+recipe+'%')
      return render_template("index.html", recipes=recipes)
    elif not name and not description and ingredients:
      recipes = db.execute("SELECT * FROM recipe WHERE ingredients LIKE ? ORDER BY RANDOM() LIMIT 10", '%'+recipe+'%')
      return render_template("index.html", recipes=recipes)
    # if only two of the boxes are checked
    elif name and description and not ingredients:
      recipes = db.execute("SELECT * FROM recipe WHERE name LIKE ? OR description LIKE ? ORDER BY RANDOM() LIMIT 10", '%'+recipe+'%', '%'+recipe+'%')
      return render_template("index.html", recipes=recipes)
    elif name and not description and ingredients:
      recipes = db.execute("SELECT * FROM recipe WHERE name LIKE ? OR ingredients LIKE ? ORDER BY RANDOM() LIMIT 10", '%'+recipe+'%', '%'+recipe+'%')  
      return render_template("index.html", recipes=recipes)  
    elif not name and description and ingredients:
      recipes = db.execute("SELECT * FROM recipe WHERE ingredients LIKE ? OR description LIKE ? ORDER BY RANDOM() LIMIT 10", '%'+recipe+'%', '%'+recipe+'%')
      return render_template("index.html", recipes=recipes)
    elif not name and not description and not ingredients:
      flash("please select at least one searching criteria")
      return redirect("/")
    
  # if the user didn't search, show the users any 10 recipes
  else:
    """Show 10 recipes"""
    recipes = db.execute("SELECT * FROM recipe ORDER BY RANDOM() LIMIT 10")
    return render_template("index.html", recipes=recipes)


if __name__ == '__main__':
  app.run(host='0.0.0.0')


# show the users the details of the recipe clicked on
@app.route("/recipe/<id>", methods=["GET", "POST"])
def recipe(id):
  recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id)
  
  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":
    user = session["user_id"]

    # check if the recipe is already in the user's favorites
    rows = db.execute("SELECT * FROM favorites WHERE recipereference = ? AND userreference = ?", id, user)
    if len(rows) == 1:
      db.execute("DELETE FROM favorites WHERE recipereference = ? AND userreference = ?", id, user)
      flash("recipe removed from favorites")
      return render_template("recipe.html", recipe=recipe)
    else:
      db.execute("INSERT INTO favorites VALUES (?, ?)", id, user)
      flash("recipe added to favorites")
      return render_template("recipe.html", recipe=recipe)

  else:
    return render_template("recipe.html", recipe=recipe)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # check the inputs
        if not username:
            flash("username required")
            return render_template("login.html")

        # Ensure password was submitted
        elif not password:
            flash("password required")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["userid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
  

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check the inputs
        if not username:
            flash("username required")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            flash("username taken")
            return render_template("register.html")

        if not password:
            flash("password required")
            return render_template("register.html")

        if confirmation != password:
            flash("password doesn't match")
            return render_template("register.html")

        # hash the password
        hash = generate_password_hash(password)

        # Remember registrant
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Redirect user to login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/contribute", methods=["GET", "POST"])
@login_required
def contribute():

  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":
      name = request.form.get("recipe_name")
      name = name.lower()
      description = request.form.get("recipe_descrip")
      description = description.lower()
      ingredients = request.form.get("recipe_ingre")
      ingredients = ingredients.lower()
      steps = request.form.get("recipe_steps")
      steps = steps.lower()
      user = session["user_id"]

      # check the inputs
      if not name:
        flash("name required")
        return render_template("contribute.html")
      
      rows = db.execute("SELECT * FROM recipe WHERE name = ?", name)
      if len(rows) == 1:
        flash("a recipe with this name already exists, please use a different name")
        return render_template("contribute.html")

      if not description:
        flash("description required")
        return render_template("contribute.html")

      if not ingredients:
        flash("ingredients required")
        return render_template("contribute.html")

      if not steps:
          flash("steps required")
          return render_template("contribute.html")

      # remember new recipe
      db.execute("INSERT INTO recipe (name, description, ingredients, steps, user, submitted) VALUES (?, ?, ?, ?, ?, CURRENT_DATE)", name, description, ingredients, steps, user)

      # Redirect user to their recipes page
      return redirect("/myrecipes")


  # User reached route via GET (as by clicking a link or via redirect)
  else:
    return render_template("contribute.html")


@app.route("/myrecipes")
@login_required
def myrecipes():
  user = db.execute("SELECT * FROM users WHERE userid = ?", session["user_id"])
  recipes = db.execute("SELECT * FROM recipe WHERE user = ? ORDER BY submitted DESC", session["user_id"])
  return render_template("myrecipes.html", user=user, recipes=recipes)


@app.route("/favorites")
@login_required
def favorites():
  user = db.execute("SELECT * FROM users WHERE userid = ?", session["user_id"])
  recipes = db.execute("SELECT * FROM recipe JOIN favorites ON recipe.id = recipereference JOIN users ON favorites.userreference = users.userid WHERE users.userid  = ?", session["user_id"])
  return render_template("favorites.html", user=user, recipes=recipes)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
  recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id)

  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":
      name = request.form.get("recipe_name")
      name = name.lower()
      description = request.form.get("recipe_descrip")
      description = description.lower()
      ingredients = request.form.get("recipe_ingre")
      ingredients = ingredients.lower()
      steps = request.form.get("recipe_steps")
      steps = steps.lower()
      user = session["user_id"]

      # check the inputs
      if not name:
        flash("name required")
        return render_template("contribute.html")

      if not description:
        flash("description required")
        return render_template("contribute.html")

      if not ingredients:
        flash("ingredients required")
        return render_template("contribute.html")

      if not steps:
          flash("steps required")
          return render_template("contribute.html")

      # remember new recipe
      db.execute("REPLACE INTO recipe (id, name, description, ingredients, steps, user, submitted) VALUES (?, ?, ?, ?, ?, ?, CURRENT_DATE)", id, name, description, ingredients, steps, user)

      # Redirect user to their recipes page
      recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id)
      return render_template("recipe.html", recipe=recipe)

  # User reached route via GET (as by clicking a link or via redirect)
  else:
    return render_template("edit.html", recipe=recipe)