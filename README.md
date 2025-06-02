# 🎬 Movie Recommendation System

This is a web-based Movie Recommendation System built using **Streamlit** and **MongoDB**. The app supports movie search, CRUD operations on movies and ratings, and user authentication.

## 🚀 Features

- 🔐 User Login & Signup
- 🔍 Search Movies by Genre (with pagination)
- ➕ Add New Movie and Rate it
- ⭐ Submit or Update Ratings
- ❌ Delete Ratings
- 📊 View Top 10 Rated Movies (with bar chart)

## 🛠 Tech Stack

- **Frontend/UI**: Streamlit
- **Database**: MongoDB
- **Backend**: Python (PyMongo)
- **Data Visualization**: Matplotlib

## 📂 Folder Structure

```
.
├── app.py                         # Main Streamlit application
├── movie_recommendation.movies.json  # Sample movie data
├── movie_recommendation.tags.json    # Sample user tags on movies
├── movies.ipynb                  # Jupyter notebook for data exploration
├── requirements.txt              # Python dependencies
```

## 📦 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/movie-recommendation-system.git
    cd movie-recommendation-system
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Make sure MongoDB is running locally (`mongodb://localhost:27017/`).

4. Run the app:
    ```bash
    streamlit run app.py
    ```

## 📥 Ratings Dataset (External)

To populate the ratings collection, download and import the file using the command below:

🔗 [Download movie_recommendation.ratings.json](https://drive.google.com/file/d/1-GPm6-Qr_xTo4pWd89j3s98AOiHSNo2d/view?usp=drive_link)


## 📌 Notes

- Ensure your MongoDB database has collections: `users`, `movies`, and `ratings`.
- Populate them using the provided `.json` files as needed.

## 📧 Contact

For issues or contributions, please open a GitHub issue or PR.

---

