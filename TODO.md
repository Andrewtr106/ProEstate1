# ProEstate Full Redevelopment — Implementation TODO

## Phase 0: Baseline validation
- [x] Inspected existing Flask frontend/templates + chatbot widget
- [x] Inspected existing FastAPI chatbot scaffold (`backend/app/*`)
- [x] Identified contract mismatch (`/chat_api` vs `/api/chatbot/message`)
- [x] Inspected current SQLite schema + init_db.py + models.py

## Phase 1: Backend unification + PostgreSQL (schema from spec)
- [ ] Create FastAPI data layer using PostgreSQL
- [ ] Drop/recreate schema per provided SQL
- [ ] Seed 30+ sample properties
- [ ] Add indexes, constraints, FK relationships
- [ ] Implement core REST APIs for properties, agents, users, saved, inquiries

## Phase 2: AI chatbot (Ollama)
- [ ] Install/start Ollama and pull `llama3`
- [ ] Implement `POST /api/chatbot/message`
  - [ ] Input: `{ message, session_id, language: "ar"|"en" }`
  - [ ] Output: `{ response, suggested_properties: [...] }`
  - [ ] Persist sessions/messages to `chatbot_sessions`
  - [ ] Inject required system prompt
- [ ] Remove/reduce legacy Flask `/chat_api` dependency

## Phase 3: Frontend redevelopment (premium + animations)
- [ ] Build bilingual UI with RTL/LTR switching
- [ ] Implement required 3D/animation elements on all pages:
  - [ ] Three.js hero scene + particle floating + parallax
  - [ ] Property cards 3D flip hover
  - [ ] 3D map section with glowing pins
  - [ ] Lottie loading screen
  - [ ] AOS + GSAP ScrollTrigger on every section
  - [ ] Animated background gradient/particles
  - [ ] Viewport counters animation
  - [ ] Navbar transparent → frosted glass on scroll
- [ ] Replace existing chatbot widget to call FastAPI endpoint

## Phase 4: Dashboard + Admin (CRUD + analytics + AI insights)
- [ ] User dashboard UI
- [ ] Admin CRUD for properties/users/agents
- [ ] Analytics dashboard (Chart.js/Recharts)
- [ ] AI insights panel (popular searches/trends)

## Phase 5: Testing + docs
- [ ] Smoke test chatbot endpoint + filtering endpoints
- [ ] Manual E2E test checklist
- [ ] README + .env.example setup instructions

---

# ProEstate Database Schema Update

## Completed Tasks
- [x] Update init_db.py to create complete database schema matching models.py
- [x] Run the updated init_db.py to recreate database
- [x] Verify database integrity with test_database.py
- [x] Ensure all required tables and columns are present

## Database Schema Status
- ✅ Users table: id, email, password, role
- ✅ Properties table: id, title, description, price, property_type, location, area, bedrooms, bathrooms, down_payment, monthly_installment, installment_years, image, created_at, updated_at, status, user_id
- ✅ Favorites table: id, user_id, property_id, created_at
- ✅ Contact_messages table: id, name, email, phone, subject, message, property_id, created_at, is_read
- ✅ Chat_history table: id, session_id, user_id, role, message, timestamp

## Sample Data Inserted
- ✅ Admin user: admin@proestate.com
- ✅ Sample user: user@example.com
- ✅ 12 demo properties with complete details
- ✅ Sample favorites, contact messages, and chat history

---

# AI Chatbot Integration for ProEstate Flask App

## Current Status
- Backend: ✅ Implemented (models, database table, API endpoint)
- Database: ✅ ChatHistory table created
- Frontend: 🔄 In Progress

## Tasks
- [ ] Create static/css/chatbot.css for responsive styling
- [ ] Create static/js/chatbot.js for functionality
- [ ] Add chatbot widget HTML to templates/base.html
- [ ] Test ChatHistory CRUD operations
- [ ] Test chatbot for anonymous users
- [ ] Test chatbot for logged-in users
- [ ] Verify responsive design
- [ ] Check for console errors
- [ ] Ensure no regressions in existing functionality

## Notes
- Backend and database are already implemented
- Focus on frontend widget integration
- Widget should be fixed bottom-left with toggle functionality
- Use session_id for anonymous users, link to user_id for logged-in users
- Check FAQ before querying OpenAI

---

# Admin Dashboard Implementation

## Tasks
- [x] Add /admin/ route in app.py for admin dashboard
- [x] Create templates/admin/index.html dashboard template
- [x] Test admin dashboard access and functionality
- [x] Verify Manage Properties functionality (CRUD operations)
