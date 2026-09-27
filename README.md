# Sentiview AI

A full-stack YouTube Comment Sentiment Analysis web application.

## Architecture
- **Frontend**: React 18, Vite, CSS Modules (Neomorphic Design)
- **Backend**: Python 3.11, FastAPI, scikit-learn NLP
- **Database**: MongoDB Atlas

## Getting Started

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
pip install -r requirements.txt
```

Set up your `.env` file in the `backend/` directory based on `backend/.env.example`. Be sure to add your MongoDB connection string.

**Train the Model**:
Place your dataset (`youtube_comments.csv`) in `backend/data/raw/` and run:
```bash
python ml/train.py
```

**Run Backend Server**:
```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The frontend will start at `http://localhost:5173`.
