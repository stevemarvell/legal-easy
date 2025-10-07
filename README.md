# legal-easy

Full-stack demo with FastAPI backend and TypeScript frontend.

## Project Structure

```
legal-easy/
├── backend/          # Python FastAPI backend
│   ├── main.py       # FastAPI application
│   ├── dev.py        # Development server script
│   └── requirements.txt
├── frontend/         # TypeScript frontend
│   ├── src/          # TypeScript source files
│   ├── public/       # Static files and build output
│   ├── dev.js        # Development script
│   └── build.js      # Build script
└── .github/workflows/ # CI/CD configuration
```

## Local Deploy

**Backend (Python 3.10+)**
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt

# Development server (auto-reload)
python dev.py
# OR manually: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Backend URL: `http://localhost:8000`

**Frontend (Node 18+)**
```bash
cd frontend
npm install

# Development (auto-rebuild on changes)
npm run dev
# OR build once: npm run build
# OR serve built files: npm run serve
```
Frontend URL: `http://localhost:8080` (when using `npm run serve`)  
Or open `frontend/public/index.html` directly in your browser.

## GitHub Deploy

1. Fork this repository
2. Set repository secrets:
   - `RAILWAY_TOKEN`
   - `RAILWAY_BACKEND_SERVICE_ID`
   - `RAILWAY_FRONTEND_SERVICE_ID`
   - `RAILWAY_BACKEND_URL` (e.g., `https://your-backend-name.railway.app`)
3. Push to main branch to trigger deployment

## Railway Deploy

**Backend:**
1. Create new Railway project
2. Connect your GitHub repository
3. Set root directory to `backend`
4. Railway will use `railway.json` configuration and `Procfile`
5. Note your backend URL: `https://your-backend-name.railway.app`

**Frontend:**
1. Create another Railway service
2. Set root directory to `frontend`
3. Railway will use `railway.json` configuration
4. Set environment variable `BACKEND_URL` to your backend URL
5. Frontend URL: `https://your-frontend-name.railway.app`

**Configuration:**
- Backend uses `Procfile` for deployment configuration
- Frontend uses `package.json` start script for deployment
- Backend URL is auto-detected locally, injected via environment variable on Railway

## API Endpoints

- `GET /` - Health check
- `GET /random` - Returns `{ "value": <0..100> }`