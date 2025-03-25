import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import io

API_KEY = "e5c26b19fe5c80a2b50c9f80e94a0850"
API_URL = "https://api.themoviedb.org/3/search/movie"

def get_movie_info(movie_name):
    params = {
        "api_key": API_KEY,
        "query": movie_name
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]
        else:
            return None
    else:
        return None
    
def display_movie():
    movie_name = entry.get()
    if not movie_name:
        messagebox.showwarning("Error", "Please enter a movie name")
        return
    
    movie = get_movie_info(movie_name)
    if movie:
        title = movie["title"]
        rating = movie["vote_average"]
        release_date = movie["release_date"]
        overview = movie["overview"]
        poster_path = movie["poster_path"]

        title_label.config(text=f"Title: {title}")
        rating_label.config(text=f"Rating: {rating}")
        release_date_label.config(text=f"Release Date: {release_date}")
        overview_label.config(text=f"Overview: {overview[:200]}...")

        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            img_data = requests.get(image_url).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((200, 300))
            img = ImageTk.PhotoImage(img)
            poster_label.config(image=img)
            poster_label.image = img
    else:
        messagebox.showerror("Error", "Movie not found")

root = tk.Tk()
root.title("Movie Search App")
root.geometry("500x600")
root.config(bg="aqua")

tk.Label(root, text="Enter Movie Name:", font=("Roboto", 12)).pack(pady=10)
entry = tk.Entry(root, width=40, font=("Roboto", 12))
entry.pack(pady=10)
search_button = tk.Button(root, text="Search", font=("Roboto", 12), command=display_movie)
search_button.pack(pady=10)

title_label = tk.Label(root, text="Title: ", font=("Roboto", 12), bg="white")
title_label.pack()

rating_label = tk.Label(root, text="Rating: ", font=("Roboto", 12), bg="white")
rating_label.pack()

release_date_label = tk.Label(root, text="Release Date: ", font=("Roboto", 12), bg="white")
release_date_label.pack()

overview_label = tk.Label(root, text="Overview: ", font=("Roboto", 12), wraplength=400, bg="white", justify="left")
overview_label.pack(pady=5)

poster_label = tk.Label(root, bg="white")
poster_label.pack(pady=10)

root.mainloop()