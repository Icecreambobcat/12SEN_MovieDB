from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import httpx
import os
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Replace with your TMDb API key
TMDB_API_KEY = "your_api_key_here"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Database setup
def init_db():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies
        (id INTEGER PRIMARY KEY,
         title TEXT NOT NULL,
         year TEXT,
         poster_path TEXT,
         rating INTEGER NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

class Movie(BaseModel):
    id: int
    title: str
    year: str = None
    poster_path: str = None
    rating: int = None

@app.get("/")
async def home(request: Request):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    movies = [
        Movie(id=row[0], title=row[1], year=row[2], poster_path=row[3], rating=row[4])
        for row in c.fetchall()
    ]
    conn.close()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "movies": movies}
    )

@app.get("/search")
async def search(request: Request, query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TMDB_BASE_URL}/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": query,
                "language": "en-US",
                "page": 1
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch movies")
        
        results = response.json()["results"]
        movies = [
            Movie(
                id=movie["id"],
                title=movie["title"],
                year=movie["release_date"][:4] if movie.get("release_date") else None,
                poster_path=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None
            )
            for movie in results[:5]  # Limit to 5 results
        ]
        
        return templates.TemplateResponse(
            "search_results.html",
            {"request": request, "movies": movies, "query": query}
        )

@app.post("/add-movie")
async def add_movie(
    movie_id: int = Form(...),
    title: str = Form(...),
    year: str = Form(None),
    poster_path: str = Form(None),
    rating: int = Form(...)
):
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO movies (id, title, year, poster_path, rating) VALUES (?, ?, ?, ?, ?)",
        (movie_id, title, year, poster_path, rating)
    )
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)