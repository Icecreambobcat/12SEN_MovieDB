# Movie Ratings Application

## Overview

This application allows users to search for movies using The Movie Database (TMDb) API, add them to a local watchlist, and assign ratings. It's built using Python, FastAPI, SQLite for the database, and Jinja2 for templating.

## Features

*   Search for movies online via the TMDb API.
*   Add movies from search results to a local database.
*   View all movies in the local watchlist.
*   Rate movies in the watchlist (1-5 stars).
*   Responsive web interface.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url-here>
    cd movie-ratings-application # Or your repository's directory name
    ```

2.  **Create and activate a virtual environment:**
    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

To use this application, you need to configure your TMDb API key:

1.  **Create an environment file:**
    In the root of the project, make a copy of the `.env.example` file and name it `.env`.
    ```bash
    cp .env.example .env
    ```

2.  **Set your API Key:**
    Open the `.env` file and replace `"your_api_key_here"` with your actual TMDb API key. You can obtain an API key by creating an account on [The Movie Database (TMDb)](https://www.themoviedb.org/documentation/api) and registering for an API key.
    ```
    TMDB_API_KEY="your_actual_tmdb_api_key"
    ```
    The application uses the `python-dotenv` library to load this configuration from the `.env` file.

## Running the Application

1.  **Start the FastAPI server:**
    Ensure your virtual environment is activated and you are in the project's root directory.
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag enables auto-reloading when code changes, which is useful for development.

2.  **Access the application:**
    Open your web browser and navigate to:
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Running Tests

To run the unit tests for the application:

1.  Ensure you have installed the development dependencies (including `pytest` and `pytest-mock`), which should be covered by `pip install -r requirements.txt`.
2.  From the project's root directory, run:
    ```bash
    pytest
    ```
    You can also run tests with more verbosity:
    ```bash
    pytest -v
    ```

## Project Structure

A brief overview of the key files and directories:
-   `main.py`: The main FastAPI application logic, including routes.
-   `database.py`: Handles database setup, models, and operations (SQLite).
-   `requirements.txt`: Lists Python dependencies for the project.
-   `.env.example`: Example environment file for API key configuration.
-   `/static`: Contains static files (CSS, JS, images) - if any are added.
-   `/templates`: HTML templates used by FastAPI for the web interface.
-   `/tests`: Contains unit and integration tests.
