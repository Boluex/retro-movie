# 🎞️ RetroToons

**RetroToons** is a web application dedicated to preserving and streaming classic cartoons from the early 1900s up to 2004. It provides a nostalgic experience for users who love vintage animation.

---

## 🚀 Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Frontend    | TypeScript + html|
| Backend     | FastAPI (Python)   |
| Database    | PostgreSQL         |
| Storage     | Supabase (for video file storage) |

---

## 📁 Features

- 🎬 Stream classic cartoons from 1900s to early 2000s  
- 🔎 Browse by year, genre, or cartoon studio  
- 🧾 Backend powered by FastAPI for fast performance  
- 🗂️ Video and asset storage using Supabase Buckets  
- 📦 PostgreSQL-backed data persistence

---

## 🔧 Installation

### ✅ Prerequisites

- Python 3.10+
- Node.js & npm
- PostgreSQL- Supabase account

---

### 🐍 Backend Setup (FastAPI)


# Clone the repo
git clone https://github.com/Boluex/retro-movie.git
cd retrotoons/backend

# Create a virtual environment
python3 -m venv myvenv
source myvenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (Alembic)
alembic upgrade head

# Start FastAPI
uvicorn main:app --reload


### 🐍 Frontend Setup (Typescript)
cd ../frontend

# Install dependencies
npm install

# Start the development server
npm run dev




