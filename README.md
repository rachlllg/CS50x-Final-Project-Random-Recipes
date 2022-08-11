# CS50 FINAL PROJECT: RANDOM RECIPES
## Video Demo:  https://youtu.be/xIcnc03fzR0
## Description:

#### Purpose
I never know what I should cook for dinner, so I created this randome recipe site using Javascript, 
Flask, and SQLite where the home page of the website shows 10 random recipe cards as inspiration for 
dinner ideas. The recipes are sourced from the Kaggle database.

#### Home Page
On the home page, each recipe card includes the name, the description, and the ingredients, 
so one can scan through these cards to see if any seems interesting. If none seems interesting, 
one can click on a button for the system to generate another random set of 10 recipes. If a recipe
sparks interest, one can click on the name of the recipe to be taken to the recipe details page,
where more information (name, submitted date, description, ingredients, and steps) on the recipe 
can be seen. On this same page, if the user is logged in, they can also add the recipe to their
favorites, or remove the recipe from their favorites. On the same page, if the user is the original
contributor of the recipe, they can also edit the recipe.

#### Search Function
On the home page, one can also search the recipe database by keywords, one can choose to search keywords by name, description, or ingredients. The system will generate a random set of 10 recipes that match the search criteria. One can then also click on the title to be taken to the details page of the recipe. One can also click on a button for the system to generate another random set of 10 recipes that match the same search criteria. The user can go back to the home page at any time using the navigation bar Home button on the top left corner.

#### Registered Users
One can register for a username and upon log in, one can contribute to the database, view a list of their contributions, as well as their favorites, each accessible via the navigation bar buttons on the top right corner.

#### Contribute
On the contribute page, a logged in user can contribute to the database by providing name, description, ingredients, and steps (all required fields) and the system will auto add the current date and an ID to the recipe when the save button is clicked. The name must not already exist in the database. Errors are displayed on the top of the page in the form of warning alerts in yellow. A user must clear all errors before the recipe can be successfully contributed to the databased.

#### My Contributions
Once a recipe is contributed, the user can go to the my contributions page where all recipes the user contributed are displayed in the form of recipe cards (similar to the home page). The user can click on the name of each recipe to view the details of the recipe, add or remove the recipe to or from their favorites, and edit the recipe.

#### Edit A Contribution
When the edit button is clicked, the user will be taken to the edit page for that recipe where the name, description, ingredients, and steps are already pre-populated. The user can make edites to the recipe as needed and the recipe will be saved by replacing the original recipe in the database when the save button is clicked.

#### My Favorites
When a user click on the favorite button of a recipe, the recipe will be added to the user's favorites if the recipe is not already in the user's favorites, or else the recipe will be removed from the user's favorites.  The favorites status are displayed on the top of the page in the form of warning alerts in yellow. The user can go to the my favorites page where all recipes the user favorited are displayed in the form of recipe cards (similar to the home page). The user can click on the name of each recipe to view the details of the recipe, and add or remove the recipe to or from their favorites.

## Description of Each File:
**Static:**
- favicon.ico: This is the fried egg icon for the site
- styles.css: The site generally uses Bootstrap for styling, but also uses this file for some additional CSS styling 

**Templates:**
- layout.html: This is the overall layout page for the entire website
- index.html: This is the home page of the website which includes a simple Javascript script for the random recipe generator
- login.html: This is the user log in page
- register.html: This is the user registration page
- recipe.html: This is the recipe details page for the specific recipe requested
- favorites.html: This is the page that displays all recipes favorited by the logged in user
- contribute.html: This is the page for logged in users to contribute new recipe to the database
- myrecipes.html: This is the page that displays all recipes contributed by the logged in user
- edit.html: This is the page for the logged in user to make any edits to the recipes they contributed

**Other:**
- app.py: This is the main python file where all main functions are defined
- helps.py: This is a helper python file where the login_required function is defined
- recipe.db: This is the SQLite database for the website

## How to Run the Program:
    1. Clone the repo to local directory
    2. Open the local directory and unzip the zip file, navigate into the main folder
    3. Within the directory, run: python3 -m pip install flask
    4. Within the directory, run: flask run
    5. Open the development server
