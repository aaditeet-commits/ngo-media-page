from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'ngo_media_secret_key_2025'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'media.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS press_releases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        release_date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS media_coverage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS image_gallery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL,
        description TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_url TEXT NOT NULL,
        description TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    # Insert default admin
    try:
        c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    except:
        pass
    # Insert sample data
    c.execute("SELECT COUNT(*) FROM press_releases")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO press_releases (title, description, release_date) VALUES (?, ?, ?)",
                  ('NGO Launches New Initiative to Support Underprivileged Children',
                   'Our NGO is excited to announce a new initiative aimed at providing education and resources to children from low-income families.',
                   '2025-01-15'))
        c.execute("INSERT INTO press_releases (title, description, release_date) VALUES (?, ?, ?)",
                  ('NGO Partners with Local Communities for Clean Water Project',
                   'In partnership with local communities, our NGO has launched a clean water initiative in rural areas.',
                   '2024-12-12'))
        c.execute("INSERT INTO media_coverage (title, url) VALUES (?, ?)",
                  ('Our NGO Featured in Global News Network', 'https://example.com/article1'))
        c.execute("INSERT INTO media_coverage (title, url) VALUES (?, ?)",
                  ('TV Interview on Our Recent Environmental Initiative', 'https://example.com/article2'))
        c.execute("INSERT INTO videos (video_url, description) VALUES (?, ?)",
                  ('https://www.youtube.com/embed/dQw4w9WgXcQ', 'NGO Impact Highlights 2024'))
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── PUBLIC MEDIA PAGE ────────────────────────────────────────────────────────

@app.route('/')
def index():
    conn = get_db()
    press_releases = conn.execute("SELECT * FROM press_releases ORDER BY release_date DESC").fetchall()
    media_coverage = conn.execute("SELECT * FROM media_coverage ORDER BY created_at DESC").fetchall()
    images = conn.execute("SELECT * FROM image_gallery ORDER BY uploaded_at DESC").fetchall()
    videos = conn.execute("SELECT * FROM videos ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return render_template('index.html',
                           press_releases=press_releases,
                           media_coverage=media_coverage,
                           images=images,
                           videos=videos)


# ─── ADMIN AUTH ───────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        admin = conn.execute("SELECT * FROM admin WHERE username=? AND password=?",
                             (username, password)).fetchone()
        conn.close()
        if admin:
            session['admin'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


# ─── ADMIN DASHBOARD ──────────────────────────────────────────────────────────

@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db()
    press_releases = conn.execute("SELECT * FROM press_releases ORDER BY release_date DESC").fetchall()
    media_coverage = conn.execute("SELECT * FROM media_coverage ORDER BY created_at DESC").fetchall()
    images = conn.execute("SELECT * FROM image_gallery ORDER BY uploaded_at DESC").fetchall()
    videos = conn.execute("SELECT * FROM videos ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return render_template('admin.html',
                           press_releases=press_releases,
                           media_coverage=media_coverage,
                           images=images,
                           videos=videos)


# ─── PRESS RELEASES CRUD ──────────────────────────────────────────────────────

@app.route('/admin/press/add', methods=['POST'])
@login_required
def add_press():
    title = request.form['title']
    date = request.form['date']
    description = request.form['description']
    conn = get_db()
    conn.execute("INSERT INTO press_releases (title, description, release_date) VALUES (?, ?, ?)",
                 (title, description, date))
    conn.commit()
    conn.close()
    flash('Press release added!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/press/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_press(id):
    conn = get_db()
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        conn.execute("UPDATE press_releases SET title=?, description=?, release_date=? WHERE id=?",
                     (title, description, date, id))
        conn.commit()
        conn.close()
        flash('Press release updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    item = conn.execute("SELECT * FROM press_releases WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('edit_press.html', item=item)


@app.route('/admin/press/delete/<int:id>')
@login_required
def delete_press(id):
    conn = get_db()
    conn.execute("DELETE FROM press_releases WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Press release deleted!', 'success')
    return redirect(url_for('admin_dashboard'))


# ─── MEDIA COVERAGE CRUD ──────────────────────────────────────────────────────

@app.route('/admin/media/add', methods=['POST'])
@login_required
def add_media():
    title = request.form['title']
    url = request.form['url']
    conn = get_db()
    conn.execute("INSERT INTO media_coverage (title, url) VALUES (?, ?)", (title, url))
    conn.commit()
    conn.close()
    flash('Media coverage added!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/media/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_media(id):
    conn = get_db()
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        conn.execute("UPDATE media_coverage SET title=?, url=? WHERE id=?", (title, url, id))
        conn.commit()
        conn.close()
        flash('Media coverage updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    item = conn.execute("SELECT * FROM media_coverage WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('edit_media.html', item=item)


@app.route('/admin/media/delete/<int:id>')
@login_required
def delete_media(id):
    conn = get_db()
    conn.execute("DELETE FROM media_coverage WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Media coverage deleted!', 'success')
    return redirect(url_for('admin_dashboard'))


# ─── IMAGE GALLERY CRUD ───────────────────────────────────────────────────────

@app.route('/admin/image/add', methods=['POST'])
@login_required
def add_image():
    if 'image' not in request.files:
        flash('No file selected!', 'danger')
        return redirect(url_for('admin_dashboard'))
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        conn = get_db()
        conn.execute("INSERT INTO image_gallery (image_path, description) VALUES (?, ?)",
                     (filename, request.form.get('description', '')))
        conn.commit()
        conn.close()
        flash('Image uploaded!', 'success')
    else:
        flash('Invalid file type!', 'danger')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/image/delete/<int:id>')
@login_required
def delete_image(id):
    conn = get_db()
    img = conn.execute("SELECT * FROM image_gallery WHERE id=?", (id,)).fetchone()
    if img:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img['image_path']))
        except:
            pass
        conn.execute("DELETE FROM image_gallery WHERE id=?", (id,))
        conn.commit()
    conn.close()
    flash('Image deleted!', 'success')
    return redirect(url_for('admin_dashboard'))


# ─── VIDEO CRUD ───────────────────────────────────────────────────────────────

@app.route('/admin/video/add', methods=['POST'])
@login_required
def add_video():
    url = request.form['video_url']
    desc = request.form.get('description', '')
    conn = get_db()
    conn.execute("INSERT INTO videos (video_url, description) VALUES (?, ?)", (url, desc))
    conn.commit()
    conn.close()
    flash('Video added!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/video/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_video(id):
    conn = get_db()
    if request.method == 'POST':
        url = request.form['video_url']
        desc = request.form.get('description', '')
        conn.execute("UPDATE videos SET video_url=?, description=? WHERE id=?", (url, desc, id))
        conn.commit()
        conn.close()
        flash('Video updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    item = conn.execute("SELECT * FROM videos WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('edit_video.html', item=item)


@app.route('/admin/video/delete/<int:id>')
@login_required
def delete_video(id):
    conn = get_db()
    conn.execute("DELETE FROM videos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Video deleted!', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
