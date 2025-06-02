import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
from bson import ObjectId

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["movie_recommendation"]
users_collection = db["users"]
movies_collection = db["movies"]
ratings_collection = db["ratings"]

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "search_page" not in st.session_state:
    st.session_state["search_page"] = 0

# Sign-Up Page
def signup_page():
    st.title("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    email = st.text_input("Enter Your Email")
    if st.button("Sign Up"):
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            st.error("Username already exists. Please choose another one.")
        else:
            users_collection.insert_one({
                "username": username,
                "password": password,
                "email": email
            })
            st.success("Sign-up successful! Please log in.")

# Login Page
def login_page():
    st.title("Login")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = user
            st.success(f"Welcome back, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

# CRUD Operations Menu
def crud_filter():
    st.title("Movie CRUD Operations")
    operation = st.sidebar.selectbox(
        "Select an Operation:",
        ["Search Movies", "Add Movie", "Submit Rating", "Delete Rating", "Top Rated Movies"]
    )
    
    if operation == "Search Movies":
        search_movies()
    elif operation == "Submit Rating":
        submit_rating()
    elif operation == "Delete Rating":
        delete_rating()
    elif operation == "Top Rated Movies":
        top_rated_movies()
    elif operation == "Add Movie":
        add_movie()
        
def add_movie():
    st.subheader("Add a New Movie")

    # Input details for the new movie
    movie_name = st.text_input("Enter Movie Name")
    genres = st.text_input("Enter Genres (comma-separated)")
    rating = st.slider("Enter Your Rating (0 to 5)", 0.0, 5.0, step=0.5)
    
    if st.button("Add Movie"):
        try:
            # Generate a unique movie ID
            movie_id = movies_collection.count_documents({}) + 1
            
            # Prepare movie document
            new_movie = {
                "movieId": movie_id,
                "title": movie_name,
                "genres": genres.split(", ")
            }
            
            # Insert the new movie into movies_collection
            movies_collection.insert_one(new_movie)

            # Prepare rating document
            user_id = st.session_state["current_user"]["_id"]
            new_rating = {
                "ratingId": str(ObjectId()),  # Unique ID for the rating
                "userId": user_id,
                "movieId": movie_id,
                "movieTitle": movie_name,
                "rating": rating
            }
            
            # Insert the rating into ratings_collection
            ratings_collection.insert_one(new_rating)

            st.success(f"Movie '{movie_name}' added successfully with your rating!")
            st.write("### New Movie Details:")
            st.write(new_movie)
            st.write("### New Rating Details:")
            st.write(new_rating)

        except Exception as e:
            st.error(f"An error occurred: {e}")


# Search for Movies by Genre with Pagination
def search_movies():
    st.subheader("Search Movies by Genre")
    genre = st.text_input("Enter a Genre")
    limit = 5
    skip = st.session_state["search_page"] * limit

    if genre:
        movies = list(movies_collection.find({"genres": {"$regex": genre, "$options": "i"}}).skip(skip).limit(limit))
        if movies:
            st.write("Movies Found:")
            for movie in movies:
                st.write(f"- {movie['title']} (Genres: {movie['genres']})")
            
            col1, col2 = st.columns(2)
            if col1.button("Previous Page"):
                if st.session_state["search_page"] > 0:
                    st.session_state["search_page"] -= 1
                    st.experimental_rerun()
            if col2.button("Next Page"):
                if len(movies) == limit:
                    st.session_state["search_page"] += 1
                    st.experimental_rerun()
        else:
            st.warning("No movies found for the specified genre.")
    else:
        st.info("Enter a genre to search for movies.")

# Submit a Rating
def submit_rating():
    st.subheader("Submit a Rating")

    # Step 1: Input user ID, movie ID, and rating
    user_id = st.text_input("Enter Your Rating Object ID")
    movie_id = st.number_input("Enter Movie ID", step=1, min_value=1)
    rating = st.slider("Rating (0 to 5)", 0.0, 5.0, step=0.5)

    if st.button("Submit Rating"):
        try:
            # Check if the movie exists in movies_collection by movieId
            movie = movies_collection.find_one({"movieId": movie_id})
            
            if movie:
                # Step 2: Check if a rating already exists for this user and movie
                existing_rating = ratings_collection.find_one({"userId": user_id, "movieId": movie_id})

                if existing_rating:
                    # Update the existing rating
                    result = ratings_collection.update_one(
                        {"_id": existing_rating["_id"]},
                        {"$set": {"rating": rating}}
                    )
                    
                    if result.modified_count > 0:
                        st.success(f"Rating updated successfully for '{movie['title']}'!")
                        st.write("### Updated Rating Details:")
                        updated_rating = ratings_collection.find_one({"_id": existing_rating["_id"]})
                        st.write(updated_rating)
                    else:
                        st.error("Failed to update the rating. Please try again.")
                else:
                    # Add a new rating
                    new_rating = {
                        "ratingId": str(ObjectId()),  # Unique ID for the rating
                        "userId": user_id,
                        "movieId": movie_id,
                        "movieTitle": movie["title"],
                        "rating": rating
                    }
                    ratings_collection.insert_one(new_rating)
                    st.success(f"New rating added successfully for '{movie['title']}'!")
                    st.write("### New Rating Details:")
                    st.write(new_rating)
            else:
                st.error(f"Movie with ID {movie_id} not found. Please check the Movie ID.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


# Delete a Rating
def delete_rating():
    st.subheader("Delete a Rating")
    rating_id = st.text_input("Enter Rating ID")
    if st.button("Delete Rating"):
        try:
            result = ratings_collection.delete_one({"_id": ObjectId(rating_id)})
            if result.deleted_count > 0:
                st.success("Rating deleted successfully!")
            else:
                st.error("Rating not found.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display Top Rated Movies
def top_rated_movies():
    st.subheader("Top Rated Movies")

    try:
        # Aggregate ratings to calculate the average rating for each movie
        top_movies = ratings_collection.aggregate([
            {"$group": {"_id": "$movieId", "avgRating": {"$avg": "$rating"}}},
            {"$sort": {"avgRating": -1}},  # Sort by average rating in descending order
            {"$limit": 10}  # Limit to top 10 movies
        ])

        # Prepare data for display
        movie_titles, avg_ratings = [], []

        for movie in top_movies:
            # Fetch movie details from movies_collection
            movie_info = movies_collection.find_one({"movieId": movie["_id"]})
            if movie_info:
                movie_titles.append(movie_info["title"])
                avg_ratings.append(movie["avgRating"])

        if movie_titles:
            # Display top-rated movies
            st.write("### Top 10 Rated Movies:")
            for i, (title, rating) in enumerate(zip(movie_titles, avg_ratings), start=1):
                st.write(f"{i}. **{title}** - Average Rating: {rating:.2f}")

            # Visualize the data
            fig, ax = plt.subplots()
            ax.barh(movie_titles, avg_ratings, color="skyblue")
            ax.set_xlabel("Average Rating")
            ax.set_ylabel("Movies")
            ax.set_title("Top Rated Movies")
            ax.invert_yaxis()  # Highest rating at the top
            st.pyplot(fig)
        else:
            st.warning("No top-rated movies available. Make sure ratings are available in the database.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Main App Logic
if not st.session_state["logged_in"]:
    option = st.sidebar.radio("Choose Option", ["Login", "Sign Up"])
    if option == "Login":
        login_page()
    elif option == "Sign Up":
        signup_page()
else:
    st.sidebar.title(f"Hello, {st.session_state['current_user']['username']}!")
    st.sidebar.write("Navigate through the app:")
    crud_filter()
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        st.experimental_rerun()
