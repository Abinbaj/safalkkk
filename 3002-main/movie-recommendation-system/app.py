from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = 'f636ea1033'

# TMDB API Key
API_KEY = '9ba93d1cf5e3054788a377f636ea1033'  

# Initialize in-memory storage for favorites and watchlist (for demonstration purposes)
user_data = {
    'watchlist': [],
    'favorites': []
}

# Function to fetch top-rated movies
def get_top_rated_movies():
    url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        for movie in results:
            movie['rating'] = movie.get('vote_average', 'N/A')
            poster_path = movie.get('poster_path')
            if poster_path:
                movie['poster'] = f"https://image.tmdb.org/t/p/w200{poster_path}"
            else:
                movie['poster'] = "https://via.placeholder.com/200x300?text=No+Image"
        return results
    else:
        return []

# Function to fetch newly released movies
def get_new_released_movies():
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        for movie in results:
            movie['rating'] = movie.get('vote_average', 'N/A')
            poster_path = movie.get('poster_path')
            if poster_path:
                movie['poster'] = f"https://image.tmdb.org/t/p/w200{poster_path}"
            else:
                movie['poster'] = "https://via.placeholder.com/200x300?text=No+Image"
        return results
    else:
        return []

# Function to fetch trending movies
def get_trending_movies():
    url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        for movie in results:
            movie['rating'] = movie.get('vote_average', 'N/A')
            poster_path = movie.get('poster_path')
            if poster_path:
                movie['poster'] = f"https://image.tmdb.org/t/p/w200{poster_path}"
            else:
                movie['poster'] = "https://via.placeholder.com/200x300?text=No+Image"
        return results
    else:
        return []

# Home route displaying trending, top-rated, and new released movies
@app.route('/')
def index():
    trending_movies = get_trending_movies()
    top_rated_movies = get_top_rated_movies()
    new_released_movies = get_new_released_movies()
    return render_template(
        'index.html',
        trending_movies=trending_movies,
        top_rated_movies=top_rated_movies,
        new_released_movies=new_released_movies
    )

# Remaining routes
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    if movie:
        return render_template('movie_details.html', movie=movie)
    else:
        return "Movie not found", 404

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    search_results = search_movie(movie_title)
    
    if search_results:
        movie_id = search_results[0]['id']
        recommendations = get_recommendations(movie_id)
        return render_template('index.html', recommendations=recommendations)
    else:
        return render_template('index.html', recommendations=[])

@app.route('/watchlist/add/<int:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    if movie_id not in user_data['watchlist']:
        user_data['watchlist'].append(movie_id)
    return redirect(url_for('view_watchlist'))

@app.route('/favorites/add/<int:movie_id>', methods=['POST'])
def add_to_favorites(movie_id):
    if movie_id not in user_data['favorites']:
        user_data['favorites'].append(movie_id)
    return redirect(url_for('view_favorites'))

@app.route('/watchlist', methods=['POST'])
def remove_from_watchlist():
    movie_id = request.form.get('movie_id')
    if movie_id and int(movie_id) in user_data['watchlist']:
        user_data['watchlist'].remove(int(movie_id))
    return redirect(url_for('view_watchlist'))

@app.route('/favorites', methods=['POST'])
def remove_from_favorites():
    movie_id = request.form.get('movie_id')
    if movie_id and int(movie_id) in user_data['favorites']:
        user_data['favorites'].remove(int(movie_id))
    return redirect(url_for('view_favorites'))

@app.route('/watchlist')
def view_watchlist():
    watchlist_ids = user_data['watchlist']
    watchlist_movies = [get_movie_details(movie_id) for movie_id in watchlist_ids if get_movie_details(movie_id)]
    return render_template('watchlist.html', watchlist=watchlist_movies)

@app.route('/favorites')
def view_favorites():
    favorite_ids = user_data['favorites']
    favorite_movies = [get_movie_details(movie_id) for movie_id in favorite_ids if get_movie_details(movie_id)]
    return render_template('favorites.html', favorites=favorite_movies)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
