# NGO Media Page – Python Flask Full Stack Project
## Assignment 5 | Code B Integrated Internship – Python

---

## 📌 Project Overview
A full-stack Python web application for managing an NGO's **Media Page**.  
Built with **Flask** (Python) + **SQLite** database + **HTML/CSS** frontend.

---

## 🚀 How to Run Locally

### 1. Clone / Download the project
```bash
git clone <your-repo-url>
cd ngo_media
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

### 4. Open in browser
- **Media Page (Public):** http://127.0.0.1:5000/
- **Admin Dashboard:** http://127.0.0.1:5000/admin
- **Admin Login:** http://127.0.0.1:5000/admin/login

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 🗄️ Database Design (SQLite)

### Tables:
| Table | Purpose |
|---|---|
| `press_releases` | Stores press release records (title, date, description) |
| `media_coverage` | Stores media coverage links (title, URL) |
| `image_gallery` | Stores uploaded image file paths |
| `videos` | Stores video URLs (YouTube embeds etc.) |
| `admin` | Stores admin login credentials |

---

## 🌐 Features

### Public Media Page (`/`)
- Introduction section
- Press Releases listing
- Media Coverage with external links
- Image Gallery with lightbox preview
- Video section with YouTube embed support
- Contact footer

### Admin Dashboard (`/admin`)
- Secure login (session-based authentication)
- **Press Releases:** Add / Edit / Delete
- **Media Coverage:** Add / Edit / Delete
- **Image Gallery:** Upload images / Delete
- **Videos:** Add / Edit / Delete

---

## 📁 Project Structure
```
ngo_media/
│
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── media.db                  # SQLite database (auto-created)
│
├── templates/
│   ├── index.html            # Public media page
│   ├── login.html            # Admin login
│   ├── admin.html            # Admin dashboard
│   ├── edit_press.html       # Edit press release
│   ├── edit_media.html       # Edit media coverage
│   └── edit_video.html       # Edit video
│
└── static/
    └── uploads/              # Uploaded images stored here
```

---

## 🚀 Deployment (Free Server – Render.com)

1. Push code to GitHub repository
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `python app.py`
6. Deploy!

---

## 👤 Author
**Aaditee** | Code B Integrated Internship – Python Full Stack  
Assignment 5: Media Page Management Module
