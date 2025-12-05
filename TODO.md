# Chatbot Implementation TODO

## Database Schema
- [x] Create ChatHistory table in SQL Server
- [x] Add ChatHistory model to models.py
- [x] Update init_db.py to create ChatHistory table

## Backend Integration
- [x] Integrate OpenAI in app.py securely
- [x] Create /chat_api route with history loading and OpenAI calls
- [x] Implement message storage (user and assistant)
- [x] Handle authenticated and anonymous users

## Frontend Widget
- [x] Modify base.html to include chatbot widget
- [x] Create chatbot.js for frontend logic
- [x] Implement floating chat icon and expandable window
- [x] Add AJAX message handling and loading indicators

## Features
- [x] Connect chatbot with user accounts/sessions
- [x] Enable navigation actions via bot responses
- [x] Implement session handling for anonymous users

## Testing
- [x] Test API endpoints
- [x] Test UI widget across all pages
- [x] Test database saving
- [x] Test anonymous and logged-in user flows
- [x] Test OpenAI responses and navigation
- [x] Ensure no regressions in existing functionality
