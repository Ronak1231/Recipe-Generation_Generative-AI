
# ⭐Recipe Generator Application

A Streamlit-based web application for generating recipes, tracking history, and providing personalized recipe recommendations. Users can filter recipes based on cuisine, diet, cooking time, and ingredients. The app also includes secure user authentication and history tracking features.

## Features

- **User Authentication**: Register and log in with secure password hashing.
- **Recipe Filters**: Search recipes by cuisine, diet, cooking time, and ingredients.
- **Personalized Recipe Suggestions**: View a randomly selected recipe based on search criteria.
- **Recipe Details**: View ingredients, instructions, and a link to the original recipe.
- **History Tracking**: Save and access your recipe history.

## Dataset

The application uses a dataset named `updated_food_dataset.csv`, containing preprocessed recipe data, including details such as:

- Recipe Name
- Cuisine
- Diet
- Cooking Time
- Ingredients
- Instructions
- Images and Original Recipe Links

---

## Installation

Follow the steps below to set up and run the application locally:

### Prerequisites

- Python 3.8 or higher
- `pip` for Python package management

### Clone the Repository

```bash
git clone https://github.com/<your-username>/recipe-generator-app.git
cd recipe-generator-app
```

### Install Required Libraries

Install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Set Up the Dataset

Ensure the dataset file `updated_food_dataset.csv` is in the root directory of the project. If not, copy it to the appropriate location.

### Initialize the Database

Run the application once to initialize the SQLite database:

```bash
python app.py
```

This step creates two tables: `users` for user credentials and `recipe_history` for storing recipe history.

---

## Usage

1. Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open the provided URL in your web browser (usually `http://localhost:8501`).

3. **Register** or **Log In** to access the application features.

4. Navigate between:
   - **Generate Recipe**: Filter and find recipes.
   - **History**: View previously searched recipes.
   - **Logout**: End your session.

---

## File Structure

```
recipe-generator-app/
├── app.py                    # Main application script
├── updated_food_dataset.csv  # Recipe dataset
├── recipe_app.db             # SQLite database (created at runtime)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Dependencies

- `streamlit` (for the user interface)
- `pandas` (for data handling)
- `sqlite3` (for database management)
- `hashlib` (for secure password hashing)
- `datetime` (for timestamp management)

Install these dependencies with:

```bash
pip install streamlit pandas
```

---

## Author

Ronak Bansal  

---

## 🙌 Contributing  
Feel free to fork this repository, make improvements, and submit a pull request.  

---

## 🐛 Troubleshooting  
If you encounter issues, please create an issue in this repository.  

---

## 📧 Contact  
For inquiries or support, contact [ronakbansal12345@gmail.com].  
