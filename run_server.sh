#!/bin/bash
# Quick start script for Linux/Mac
# Activates virtual environment and runs Django server

echo "Activating virtual environment..."
source venv/bin/activate

echo "Navigating to Django project directory..."
cd mfukoni_web

echo "Starting Django development server..."
echo ""
echo "Server will start at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver
