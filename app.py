import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('recipe_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS recipe_history
                 (username TEXT, recipe_name TEXT, ingredients TEXT, 
                  instructions TEXT, image_url TEXT, recipe_url TEXT, 
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('updated_food_dataset.csv')
    return df

# Security functions
def make_hashed_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password(password, hashed_password):
    return make_hashed_password(password) == hashed_password

# Database operations
def add_user(username, password):
    conn = sqlite3.connect('recipe_app.db')
    c = conn.cursor()
    hashed_password = make_hashed_password(password)
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect('recipe_app.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result is not None:
        return check_password(password, result[0])
    return False

def save_recipe_to_history(username, recipe):
    conn = sqlite3.connect('recipe_app.db')
    c = conn.cursor()
    
    recipe_name = recipe.get('TranslatedRecipeName', '')
    ingredients = recipe.get('TranslatedIngredients', '')
    instructions = recipe.get('TranslatedInstructions', '')
    image_url = recipe.get('image-url', '')
    recipe_url = recipe.get('URL', '')
    
    c.execute("""INSERT INTO recipe_history VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (username, recipe_name, ingredients, instructions, 
               image_url, recipe_url, datetime.now()))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect('recipe_app.db')
    query = """SELECT recipe_name, ingredients, instructions, image_url, 
               recipe_url, timestamp FROM recipe_history WHERE username=?
               ORDER BY timestamp DESC"""
    df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()
    return df

def display_recipe(recipe):
    try:
        # Recipe Name
        if 'TranslatedRecipeName' in recipe and pd.notnull(recipe['TranslatedRecipeName']):
            st.subheader(recipe['TranslatedRecipeName'])
        
        # Image
        if 'image-url' in recipe and pd.notnull(recipe['image-url']):
            try:
                st.image(recipe['image-url'], use_column_width=True)
            except:
                st.write("Image not available")
        
        # Basic Information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Cuisine' in recipe and pd.notnull(recipe['Cuisine']):
                st.write("**Cuisine:**", recipe['Cuisine'])
        
        with col2:
            if 'TotalTimeInMins' in recipe and pd.notnull(recipe['TotalTimeInMins']):
                st.write("**Total Time:**", f"{recipe['TotalTimeInMins']} minutes")
        
        with col3:
            if 'Diet' in recipe and pd.notnull(recipe['Diet']):
                st.write("**Diet:**", recipe['Diet'])
        
        # Ingredients
        if 'TranslatedIngredients' in recipe and pd.notnull(recipe['TranslatedIngredients']):
            st.write("### Ingredients")
            ingredients_list = str(recipe['TranslatedIngredients']).split(',')
            for ingredient in ingredients_list:
                st.write(f"- {ingredient.strip()}")
        
        # Instructions
        if 'TranslatedInstructions' in recipe and pd.notnull(recipe['TranslatedInstructions']):
            st.write("### Instructions")
            instructions_list = str(recipe['TranslatedInstructions']).split('.')
            for i, instruction in enumerate(instructions_list, 1):
                if instruction.strip():
                    st.write(f"{i}. {instruction.strip()}")
        
        # Recipe URL
        if 'URL' in recipe and pd.notnull(recipe['URL']):
            st.write("---")
            st.write("[View Original Recipe](%s)" % recipe['URL'])
            
    except Exception as e:
        st.error(f"Error displaying recipe: {str(e)}")

def main():
    st.set_page_config(page_title="Recipe Generator", layout="wide")
    
    # Initialize database
    init_db()
    
    # Load data
    df = load_data()
    
    # Session state initialization
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Sidebar navigation
    if st.session_state.logged_in:
        st.sidebar.title(f"Welcome {st.session_state.username}!")
        menu = st.sidebar.radio("Navigation", ["Generate Recipe", "History", "Logout"])
    else:
        menu = st.sidebar.radio("Navigation", ["Login", "Register"])
    
    if menu == "Login":
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if check_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    elif menu == "Register":
        st.title("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Register"):
            if add_user(username, password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists!")
    
    elif menu == "Generate Recipe":
        st.title("Recipe Generator")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cuisine = st.selectbox("Select Cuisine", ['All'] + sorted(df['Cuisine'].dropna().unique().tolist()))
        
        with col2:
            diet = st.selectbox("Select Diet", ['All'] + sorted(df['Diet'].dropna().unique().tolist()))
        
        with col3:
            max_time = st.number_input("Maximum Cooking Time (minutes)", min_value=0, value=120)
        
        # Search functionality
        search_term = st.text_input("Search by ingredients (comma-separated)")
        
        if st.button("Generate Recipe"):
            filtered_df = df.copy()
            
            # Apply filters
            if cuisine != 'All':
                filtered_df = filtered_df[filtered_df['Cuisine'] == cuisine]
            
            if diet != 'All':
                filtered_df = filtered_df[filtered_df['Diet'] == diet]
            
            if max_time > 0:
                filtered_df = filtered_df[filtered_df['TotalTimeInMins'] <= max_time]
            
            # Search by ingredients
            if search_term:
                search_terms = [term.strip() for term in search_term.split(',')]
                filtered_df = filtered_df[filtered_df['TranslatedIngredients'].apply(lambda x: any(term in x for term in search_terms))]
            
            # Select a random recipe
            if not filtered_df.empty:
                recipe = filtered_df.sample().iloc[0].to_dict()
                display_recipe(recipe)
                save_recipe_to_history(st.session_state.username, recipe)
            else:
                st.error("No recipes found matching your criteria!")
    
    elif menu == "History":
        st.title("Recipe History")
        history_df = get_user_history(st.session_state.username)
        st.write(history_df)
    
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully!")
        st.rerun()

if __name__ == "__main__":
    main()