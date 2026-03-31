# project-py3
# AI Recipe Generator

This project is a simple full-stack web application that generates recipes using AI.

The user selects whether the recipe should be vegetarian and enters a list of ingredients. The frontend sends this data to a FastAPI backend, which uses the Gemini API to generate recipes and returns them as JSON. The results are then displayed on the page.

## Features

* Generate recipes based on ingredients
* Vegetarian filter
* AI-powered responses (Gemini)
* Simple web interface (HTML, CSS, JavaScript)
* FastAPI backend with REST API

## Tech Stack

* Backend: FastAPI (Python)
* Frontend: HTML, CSS, JavaScript
* Database: SQLite (for basic storage)
* AI: Gemini API

## How it works

1. User enters ingredients and selects preferences
2. Frontend sends a POST request to `/ai-recipes`
3. Backend calls the AI model
4. Recipes are returned and displayed on the page

## Notes

This project was built as a backend-focused application with a simple frontend to interact with the API.
