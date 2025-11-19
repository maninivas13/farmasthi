# Integration Testing Guide

## ✅ Integration Complete!

The frontend and backend are now fully integrated. Here's what was updated:

### Changes Made:

1. **auth.js** - Updated to use backend API endpoints:
   - `registerFarmer()` now calls `/api/auth/register`
   - `loginOfficer()` now calls `/api/auth/login`
   - `verifyToken()` calls `/api/auth/me`
   - `logout()` properly cleans up tokens and WebSocket connection

2. **login.html** - Updated authentication handlers:
   - Made form submissions async to handle API calls
   - Added loading indicators
   - Improved error handling

3. **main.js** - Added backend integration functions:
   - `generateAIResponse()` - Calls `/api/ai-analysis`
   - `saveAndFinish()` - Submits queries to `/api/queries/submit`
   - `detectUrgency()`, `readFileAsDataURL()`, etc.
   - Uploads images/audio to backend endpoints

4. **dashboard.js** - Updated logout to use auth system

5. **auth.py** - Fixed import issue for `get_current_user`

## Testing Steps:

### 1. Start Backend Server
```bash
cd backend
python run.py
```
Backend should start on: http://localhost:8000

### 2. Start Frontend Server
```bash
cd frontend
start_frontend.bat
```
Or use: `python -m http.server 8080`

Frontend should be on: http://localhost:8080

### 3. Test Farmer Registration
1. Go to http://localhost:8080/login.html
2. Fill in Farmer Portal form:
   - Name: Test Farmer
   - Phone: 9876543210
   - Location: Test Village
3. Click "Continue as Farmer"
4. Should redirect to index.html with token stored

### 4. Test Query Submission
1. On index.html, scroll to "Ask a Query" section
2. Fill in query details
3. Submit query
4. Check browser console - should see API call to backend

### 5. Test Officer Login
1. Go to login.html
2. Fill in Officer Portal form:
   - Name: Test Officer
   - Department: Agricultural Extension
   - Code: OFFICER123
3. Click "Login as Officer"
4. Should redirect to dashboard.html

## API Endpoints Being Used:

### Authentication:
- POST `/api/auth/register` - Farmer registration
- POST `/api/auth/login` - Officer login
- GET `/api/auth/me` - Get current user

### Queries:
- POST `/api/queries/submit` - Submit new query
- GET `/api/queries/history` - Get query history

### Uploads:
- POST `/api/upload/image` - Upload crop images
- POST `/api/upload/voice` - Upload voice recordings

### AI Features:
- POST `/api/ai-analysis` - Get AI preliminary analysis
- POST `/api/chat/message` - AI chatbot

### WebSocket:
- WS `/ws/notifications?token=<token>` - Real-time notifications

## Troubleshooting:

### Backend not connecting:
- Check if backend is running on port 8000
- Check MongoDB connection in .env file
- Check console for CORS errors

### Registration fails:
- Check browser console for error messages
- Verify backend API is responding at /api/auth/register
- Check if phone number is already registered

### Token issues:
- Clear localStorage and try again
- Check if token is being stored (localStorage.getItem('agri_token'))
- Verify backend JWT secret is set in .env

## Next Steps:

The integration is complete! You can now:
1. Start both servers
2. Test the full flow: Register → Login → Submit Query → Get Response
3. Add more features like real-time notifications via WebSocket
4. Implement query assignment and reply features for officers
