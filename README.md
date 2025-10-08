# legal-easy

Full-stack demo with FastAPI backend and React TypeScript frontend built with Vite.

## Project Structure

```
legal-easy/
├── backend/          # Python FastAPI backend
│   ├── main.py       # FastAPI application
│   ├── dev.py        # Development server script
│   └── requirements.txt
├── frontend/         # React TypeScript frontend (Vite)
│   ├── src/          # React components and TypeScript source
│   ├── public/       # Static assets
│   ├── vite.config.ts # Vite configuration
│   └── package.json  # Node.js dependencies
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

# Development server with hot reload
npm run dev
# OR build for production: npm run build
# OR preview production build: npm run preview
```
Frontend URL: `http://localhost:8080` (Vite dev server with hot reload)

## Railway Deploy

**Backend:**
1. Create new Railway project
2. Connect your GitHub repository
3. Set root directory to `backend`
4. Railway will use `railway.json` configuration and `Procfile`
5. Note your backend URL: `https://legal-easy-backend-production.up.railway.app/`

**Frontend:**
1. Create another Railway service
2. Set root directory to `frontend`
3. Set environment variables:
   - `BACKEND_URL` to your backend URL
4. Frontend URL: `https://legal-easy-frontend-production.up.railway.app/`

**Configuration:**
- Backend uses `Procfile` for deployment configuration
- Frontend uses Vite build system with `package.json` start script for deployment
- Backend URL is auto-detected locally, injected via environment variable on Railway

## API Endpoints

- `GET /` - Health check
- `GET /random` - Returns `{ "value": <0..100> }`