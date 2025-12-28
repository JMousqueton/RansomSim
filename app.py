import os
import sqlite3
import random
import string
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from werkzeug.utils import secure_filename
import logging

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Configure basic logging if not configured elsewhere
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# GENERATOR FUNCTIONS AND CLASSES
# ============================================================================

def generate_random_id(length=16):
    """Generate random ID with 16 characters (mix of letters and numbers)"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class DocumentNameGenerator:
    """Generate realistic fake document names based on language"""
    
    def __init__(self, language='UK'):
        self.language = language
        self.uk_docs = [
            'National_Insurance_Number_{}.pdf',
            'Driving_Licence_{}.pdf',
            'Passport_Scan_{}.pdf',
            'Tax_Return_{}.pdf',
            'Bank_Statement_{}.pdf',
            'Utility_Bill_{}.pdf',
            'Employment_Contract_{}.pdf',
            'Medical_Records_{}.pdf',
            'Insurance_Policy_{}.pdf',
            'Property_Deed_{}.pdf',
            'Salary_Increase_Record_{}.xlsx',
            'Redundancy_Plan_{}.docx',
            'Restructuring_Strategy_{}.pdf',
            'Board_Minutes_{}.docx',
            'Strategic_Plan_{}.xlsx',
            'Merger_Acquisition_Details_{}.pdf',
            'Financial_Forecast_{}.xlsx',
            'Executive_Compensation_{}.xlsx',
            'Layoff_List_{}.xlsx',
            'Confidential_Agreement_{}.pdf'
        ]
        
        self.fr_docs = [
            'Numero_Securite_Sociale_{}.pdf',
            'Carte_Nationale_{}.pdf',
            'Passeport_{}.pdf',
            'Declaration_Impots_{}.pdf',
            'Releve_Bancaire_{}.pdf',
            'Facture_EDF_{}.pdf',
            'Contrat_Travail_{}.pdf',
            'Dossier_Medical_{}.pdf',
            'Attestation_Assurance_{}.pdf',
            'Acte_Propriete_{}.pdf',
            'Augmentations_Salaires_{}.xlsx',
            'Reduction_Effectifs_{}.docx',
            'Plan_Restructuration_{}.pdf',
            'Proces_Verbal_Reunion_{}.docx',
            'Strategie_Entreprise_{}.xlsx',
            'Details_Fusion_Acquisition_{}.pdf',
            'Previsions_Financieres_{}.xlsx',
            'Salaires_Cadres_{}.xlsx',
            'Liste_Licenciements_{}.xlsx',
            'Accord_Confidentialite_{}.pdf'
        ]
        
        self.de_docs = [
            'Personalausweis_{}.pdf',
            'Reisepass_{}.pdf',
            'Steuererklarung_{}.pdf',
            'Kontoauszug_{}.pdf',
            'Stromrechnung_{}.pdf',
            'Arbeitsvertrag_{}.pdf',
            'Krankenakte_{}.pdf',
            'Versicherungspolice_{}.pdf',
            'Grundbuchauszug_{}.pdf',
            'Rentenbescheid_{}.pdf',
            'Gehalterhoehungen_{}.xlsx',
            'Abbauplan_{}.docx',
            'Reorganisationsstrategie_{}.pdf',
            'Sitzungsprotokoll_{}.docx',
            'Unternehmensplan_{}.xlsx',
            'Fusionsdetails_{}.pdf',
            'Finanzprognose_{}.xlsx',
            'Geschaeftsfuehrerverguetung_{}.xlsx',
            'Kuendigungsliste_{}.xlsx',
            'Geheimhaltungsvereinbarung_{}.pdf'
        ]
        
        self.uk_passwords = [
            'pwd_admin_{}.xlsx',
            'credentials_{}.xlsx',
            'passwords_{}.xlsx',
            'access_keys_{}.docx',
            'database_creds_{}.xlsx',
            'ftp_login_{}.docx',
            'email_passwords_{}.xlsx',
            'vpn_config_{}.pdf',
            'root_access_{}.docx',
            'system_passwords_{}.xlsx'
        ]
        
        self.fr_passwords = [
            'mdp_admin_{}.xlsx',
            'identifiants_{}.xlsx',
            'mots_de_passe_{}.xlsx',
            'cles_acces_{}.docx',
            'base_donnees_{}.xlsx',
            'connexion_ftp_{}.docx',
            'emails_{}.xlsx',
            'config_vpn_{}.pdf',
            'acces_root_{}.docx',
            'mots_passes_systeme_{}.xlsx'
        ]
        
        self.de_passwords = [
            'pwd_admin_{}.xlsx',
            'anmeldedaten_{}.xlsx',
            'passworter_{}.xlsx',
            'zugangssclussel_{}.docx',
            'datenbank_pwd_{}.xlsx',
            'ftp_login_{}.docx',
            'email_passworter_{}.xlsx',
            'vpn_konfiguration_{}.pdf',
            'root_zugang_{}.docx',
            'system_passworter_{}.xlsx'
        ]
    
    def generate(self):
        """Generate a random document name"""
        doc_type = random.randint(1, 2)  # 1=document, 2=password file
        random_suffix = generate_random_id(8)
        
        if self.language == 'FR':
            docs = self.fr_docs if doc_type == 1 else self.fr_passwords
        elif self.language == 'DE':
            docs = self.de_docs if doc_type == 1 else self.de_passwords
        else:  # UK
            docs = self.uk_docs if doc_type == 1 else self.uk_passwords
        
        template = random.choice(docs)
        return template.format(random_suffix)

class FileNameGenerator:
    """Generate realistic fake file names based on language and extension"""
    
    def __init__(self, language='UK'):
        self.language = language
        self.uk_prefixes = [
            'data', 'records', 'files', 'backup', 'export', 'archive',
            'document', 'report', 'database', 'logs', 'config', 'source'
        ]
        
        self.fr_prefixes = [
            'donnees', 'dossiers', 'fichiers', 'sauvegarde', 'export', 'archive',
            'document', 'rapport', 'base_donnees', 'journaux', 'config', 'source'
        ]
        
        self.de_prefixes = [
            'daten', 'datensatze', 'dateien', 'sicherung', 'export', 'archiv',
            'dokument', 'bericht', 'datenbank', 'protokolle', 'konfiguration', 'quellen'
        ]
    
    def generate(self, extension='xlsx'):
        """Generate a random file name with given extension"""
        if self.language == 'FR':
            prefix = random.choice(self.fr_prefixes)
        elif self.language == 'DE':
            prefix = random.choice(self.de_prefixes)
        else:  # UK
            prefix = random.choice(self.uk_prefixes)
        
        random_suffix = generate_random_id(6)
        timestamp = random.randint(20200101, 20241231)
        
        return f"{prefix}_{random_suffix}_{timestamp}.{extension}"

# ============================================================================
# FLASK APPLICATION CONFIGURATION
# ============================================================================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

# Admin password from environment
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_admin():
    """Check if user is authenticated as admin"""
    return session.get('is_admin', False)

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('ransomsim.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  logo_path TEXT,
                  description TEXT,
                  language TEXT NOT NULL,
                  document_names TEXT,
                  file_names TEXT,
                  sector TEXT,
                  ransom_amount TEXT,
                  deadline_date TEXT,
                  auto_respond TEXT DEFAULT '1',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Add auto_respond column if it doesn't exist (migration for existing databases)
    try:
        c.execute('ALTER TABLE posts ADD COLUMN auto_respond TEXT DEFAULT "1"')
    except sqlite3.OperationalError:
        # Column already exists, no action needed
        pass
    
    conn.commit()
    conn.close()

def init_chat_db():
    """Initialize chat database"""
    conn = sqlite3.connect('ransomsim-chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  victim_id TEXT NOT NULL,
                  sender TEXT NOT NULL,
                  message TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_message(victim_id, sender, message):
    """Save a chat message"""
    conn = sqlite3.connect('ransomsim-chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (victim_id, sender, message) VALUES (?, ?, ?)',
              (victim_id, sender, message))
    conn.commit()
    conn.close()

def get_messages(victim_id):
    """Get all messages for a victim"""
    conn = sqlite3.connect('ransomsim-chat.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE victim_id = ? ORDER BY created_at ASC', (victim_id,))
    messages = c.fetchall()
    conn.close()
    return messages

def get_chat_summary():
    """Get summary of all chats with message count and last message date"""
    conn = sqlite3.connect('ransomsim-chat.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT victim_id, 
                        COUNT(*) as message_count,
                        MAX(created_at) as last_message_date
                 FROM messages 
                 GROUP BY victim_id 
                 ORDER BY last_message_date DESC''')
    summaries = c.fetchall()
    conn.close()
    return summaries

def delete_chat_messages(victim_id):
    """Delete all messages for a victim"""
    conn = sqlite3.connect('ransomsim-chat.db')
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE victim_id = ?', (victim_id,))
    conn.commit()
    conn.close()
    conn.close()

def get_db_posts():
    """Get all posts from database"""
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY created_at DESC')
    posts = c.fetchall()
    conn.close()
    return posts

def save_post(post_id, name, logo_path, description, language, document_names, file_names, sector=None, ransom_amount=None, deadline_date=None, auto_respond='1'):
    """Save post to database"""
    conn = sqlite3.connect('ransomsim.db')
    c = conn.cursor()
    c.execute('''INSERT INTO posts (id, name, logo_path, description, language, document_names, file_names, sector, ransom_amount, deadline_date, auto_respond)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (post_id, name, logo_path, description, language, ','.join(document_names), ','.join(file_names), sector, ransom_amount, deadline_date, auto_respond))
    conn.commit()
    conn.close()

def delete_post(post_id):
    """Delete post from database"""
    conn = sqlite3.connect('ransomsim.db')
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

def update_post(post_id, name, description, language, sector, ransom_amount, deadline_date, auto_respond='1', logo_path=None):
    """Update post in database"""
    conn = sqlite3.connect('ransomsim.db')
    c = conn.cursor()
    if logo_path is not None:
        c.execute('''UPDATE posts 
                     SET name = ?, description = ?, language = ?, sector = ?, ransom_amount = ?, deadline_date = ?, auto_respond = ?, logo_path = ?
                     WHERE id = ?''',
                  (name, description, language, sector, ransom_amount, deadline_date, auto_respond, logo_path, post_id))
    else:
        c.execute('''UPDATE posts 
                     SET name = ?, description = ?, language = ?, sector = ?, ransom_amount = ?, deadline_date = ?, auto_respond = ?
                     WHERE id = ?''',
                  (name, description, language, sector, ransom_amount, deadline_date, auto_respond, post_id))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Display all generated posts"""
    posts = get_db_posts()
    posts_list = [dict(row) for row in posts]
    for post in posts_list:
        post['documents'] = post['document_names'].split(',') if post['document_names'] else []
        post['files'] = post['file_names'].split(',') if post['file_names'] else []
    return render_template('index.html', posts=posts_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Successfully logged in as admin', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout admin"""
    session.pop('is_admin', None)
    flash('Successfully logged out', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    """Admin dashboard"""
    if not is_admin():
        flash('Please login to access admin panel', 'warning')
        return redirect(url_for('login'))
    
    posts = get_db_posts()
    posts_list = [dict(row) for row in posts]
    for post in posts_list:
        post['documents'] = post['document_names'].split(',') if post['document_names'] else []
        post['files'] = post['file_names'].split(',') if post['file_names'] else []
    return render_template('admin.html', posts=posts_list)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate a new ransomware leak site post"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            language = request.form.get('language', 'UK')
            logo_file = request.files.get('logo')
            num_documents = int(request.form.get('num_documents', 15))
            deadline_date = request.form.get('deadline_date', '')
            sector = request.form.get('sector', '')
            ransom_amount = request.form.get('ransom_amount', '')
            auto_respond = '1' if request.form.get('auto_respond') else '0'
            
            # Validate inputs
            if not name:
                return jsonify({'error': 'Name is required'}), 400
            if num_documents < 1 or num_documents > 15:
                num_documents = min(max(num_documents, 1), 15)
            
            # Generate ID
            post_id = generate_random_id()
            
            # Handle logo upload
            logo_path = None
            if logo_file and allowed_file(logo_file.filename):
                # Get file extension
                ext = logo_file.filename.rsplit('.', 1)[1].lower()
                filename = f"{post_id}.{ext}"
                logo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo_path = f"/uploads/{filename}"
            
            # Generate document names
            doc_gen = DocumentNameGenerator(language)
            document_names = [doc_gen.generate() for _ in range(num_documents)]
            
            # Generate file names
            file_gen = FileNameGenerator(language)
            file_names = []
            for _ in range(num_documents):
                extensions = ['xlsx', 'docx', 'pdf']
                file_names.append(file_gen.generate(random.choice(extensions)))
            
            # Save to database
            save_post(post_id, name, logo_path, description, language, document_names, file_names, sector if sector else None, ransom_amount if ransom_amount else None, deadline_date if deadline_date else None, auto_respond)
            
            return jsonify({
                'success': True,
                'id': post_id,
                'redirect': url_for('admin')
            })
        except Exception as e:
            logger.exception("Error while generating ransomware leak site post")
            return jsonify({'error': 'An internal error has occurred.'}), 500
    
    return render_template('generate.html')

@app.route('/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    """Edit an existing post"""
    if not is_admin():
        flash('Please login to edit posts', 'warning')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    conn.close()
    
    if not post:
        flash('Post not found', 'danger')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        language = request.form.get('language', 'UK')
        deadline_date = request.form.get('deadline_date', '')
        sector = request.form.get('sector', '')
        ransom_amount = request.form.get('ransom_amount', '')
        auto_respond = '1' if request.form.get('auto_respond') else '0'
        logo_file = request.files.get('logo')
        
        if not name:
            flash('Name is required', 'danger')
            return redirect(url_for('edit', post_id=post_id))
        
        # Handle logo upload if provided
        logo_path = None
        if logo_file and logo_file.filename and allowed_file(logo_file.filename):
            # Get file extension
            ext = logo_file.filename.rsplit('.', 1)[1].lower()
            filename = f"{post_id}.{ext}"
            logo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logo_path = f"/uploads/{filename}"
        
        update_post(post_id, name, description, language, sector if sector else None, ransom_amount if ransom_amount else None, deadline_date if deadline_date else None, auto_respond, logo_path)
        flash('Post updated successfully', 'success')
        return redirect(url_for('admin'))
    
    post_dict = dict(post)
    return render_template('edit.html', post=post_dict)

@app.route('/post/<post_id>')
def view_post(post_id):
    """View a specific post"""
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    conn.close()
    
    if not post:
        return redirect(url_for('index'))
    
    post_dict = dict(post)
    post_dict['documents'] = post_dict['document_names'].split(',') if post_dict['document_names'] else []
    post_dict['files'] = post_dict['file_names'].split(',') if post_dict['file_names'] else []
    
    # Add 3 random password files to the file list
    doc_generator = DocumentNameGenerator(language=post_dict['language'])
    password_files = [doc_generator.generate() for _ in range(3)]
    post_dict['files'].extend(password_files)
    
    return render_template('post.html', post=post_dict)

@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    """Delete a post"""
    if not is_admin():
        flash('Please login to delete posts', 'warning')
        return redirect(url_for('login'))
    
    delete_post(post_id)
    flash('Post deleted successfully', 'success')
    return redirect(url_for('admin'))

@app.route('/generate-ransomnote/<post_id>')
def generate_ransomnote(post_id):
    """Generate ransom note for a specific victim"""
    if not is_admin():
        flash('Please login to generate ransom notes', 'warning')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    conn.close()
    
    if not post:
        flash('Post not found', 'danger')
        return redirect(url_for('admin'))
    
    # Generate ransom note content
    contact_url = request.host_url.rstrip('/') + url_for('chat', victim_id=post_id)
    
    ransom_note = f"""╔══════════════════════════════════════════════════════════════╗
║                    YOUR DATA HAS BEEN ENCRYPTED              ║
╚══════════════════════════════════════════════════════════════╝

Dear {post['name']},

Your network has been compromised and all your critical data has been 
encrypted using military-grade encryption algorithms.

WHAT HAPPENED?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We have successfully infiltrated your systems and encrypted all your
sensitive files, databases, and backups. Additionally, we have 
exfiltrated {post['file_names'].count(',') + 1 if post['file_names'] else 0} GB of confidential data.

WHAT DATA WAS STOLEN?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We have obtained sensitive documents including:
"""
    
    if post['file_names']:
        files = post['file_names'].split(',')
        for i, file in enumerate(files[:5], 1):
            ransom_note += f"\n  • {file}"
    
    ransom_note += f"""

WHAT WILL HAPPEN IF YOU DON'T PAY?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
If payment is not received within the deadline:
  1. All stolen data will be published on our leak site
  2. Data will be sold to competitors and interested parties
  3. Your clients/partners will be notified of the breach
  4. Decryption will become IMPOSSIBLE

HOW TO CONTACT US?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To negotiate and receive decryption keys, visit our secure chat:

    {contact_url}

Your Unique Victim ID: {post_id}

IMPORTANT WARNINGS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠ Do NOT contact law enforcement - it will result in data publication
  ⚠ Do NOT attempt to decrypt files yourself - you will lose data
  ⚠ Do NOT delete this message - you need it to contact us
  ⚠ Do NOT ignore this - the deadline is FINAL

Time is running out. Contact us now to prevent data publication.

╔══════════════════════════════════════════════════════════════╗
║  This is an automated message. Victim ID: {post_id}          ║
╚══════════════════════════════════════════════════════════════╝

[DISCLAIMER: This ransom note is for educational and training purposes only.]
"""
    
    # Save to temporary file
    import io
    ransom_file = io.BytesIO()
    ransom_file.write(ransom_note.encode('utf-8'))
    ransom_file.seek(0)
    
    return send_file(
        ransom_file,
        mimetype='text/plain',
        as_attachment=True,
        download_name=f'RANSOM_NOTE_{post_id}.txt'
    )

@app.route('/chat', methods=['GET', 'POST'])
def chat_login():
    """Chat login page - ask for victim ID"""
    if request.method == 'POST':
        victim_id = request.form.get('victim_id', '').strip()
        if not victim_id:
            flash('Please enter your Victim ID', 'danger')
            return redirect(url_for('chat_login'))
        
        # Verify victim exists
        conn = sqlite3.connect('ransomsim.db')
        c = conn.cursor()
        c.execute('SELECT id FROM posts WHERE id = ?', (victim_id,))
        if not c.fetchone():
            conn.close()
            flash('Invalid Victim ID. Please check your ransom note.', 'danger')
            return redirect(url_for('chat_login'))
        conn.close()
        
        return redirect(url_for('chat', victim_id=victim_id))
    
    return render_template('chat_login.html')

@app.route('/chat/<victim_id>')
def chat(victim_id):
    """Chat page for victim to contact ransomware gang"""
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (victim_id,))
    post = c.fetchone()
    conn.close()
    
    if not post:
        return render_template('404.html'), 404
    
    messages = get_messages(victim_id)
    return render_template('chat.html', victim_id=victim_id, victim_name=post['name'], messages=messages)

@app.route('/chat/<victim_id>/send', methods=['POST'])
def send_message(victim_id):
    """Send a message from victim"""
    message = request.form.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Verify victim exists
    conn = sqlite3.connect('ransomsim.db')
    c = conn.cursor()
    c.execute('SELECT id FROM posts WHERE id = ?', (victim_id,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Victim not found'}), 404
    conn.close()
    
    save_message(victim_id, 'victim', message)

    # Auto-responder: generate a negotiation/playbook reply with random delay
    try:
        from libchat import generate_auto_response
        delay_min = int(os.getenv('CHAT_REPLY_DELAY_MIN', 2))
        delay_max = int(os.getenv('CHAT_REPLY_DELAY_MAX', 10))

        def _delayed_reply():
            delay = random.randint(delay_min, delay_max)
            time.sleep(delay)
            auto_reply = generate_auto_response(victim_id, message)
            if auto_reply:
                save_message(victim_id, 'gang', auto_reply)

        threading.Thread(target=_delayed_reply, daemon=True).start()
    except Exception:
        # Fail silently to avoid breaking chat delivery
        pass

    return jsonify({'success': True})

@app.route('/chat/<victim_id>/messages')
def get_chat_messages(victim_id):
    """Get all messages for a victim (API endpoint)"""
    messages = get_messages(victim_id)
    return jsonify([{
        'id': msg['id'],
        'sender': msg['sender'],
        'message': msg['message'],
        'created_at': msg['created_at']
    } for msg in messages])

@app.route('/admin/chat')
def admin_chat():
    """Admin chat dashboard showing all victims"""
    if not is_admin():
        flash('Please login to access chat management', 'warning')
        return redirect(url_for('login'))
    
    # Get chat summaries
    summaries = get_chat_summary()
    
    # Enhance with victim details
    chat_list = []
    for summary in summaries:
        conn = sqlite3.connect('ransomsim.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT name, logo_path FROM posts WHERE id = ?', (summary['victim_id'],))
        victim = c.fetchone()
        conn.close()
        
        if victim:
            chat_list.append({
                'victim_id': summary['victim_id'],
                'victim_name': victim['name'],
                'logo_path': victim['logo_path'],
                'message_count': summary['message_count'],
                'last_message_date': summary['last_message_date']
            })
    
    return render_template('admin_chat.html', chats=chat_list)

@app.route('/admin/chat/<victim_id>')
def admin_chat_detail(victim_id):
    """Admin view of specific victim chat"""
    if not is_admin():
        flash('Please login to access chat management', 'warning')
        return redirect(url_for('login'))
    
    # Get victim info
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (victim_id,))
    post = c.fetchone()
    conn.close()
    
    if not post:
        flash('Victim not found', 'danger')
        return redirect(url_for('admin_chat'))
    
    messages = get_messages(victim_id)
    return render_template('admin_chat_detail.html', victim_id=victim_id, victim_name=post['name'], messages=messages)

@app.route('/admin/chat/<victim_id>/send', methods=['POST'])
def admin_send_message(victim_id):
    """Send a message from admin (ransomware gang)"""
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    message = request.form.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    save_message(victim_id, 'gang', message)
    return jsonify({'success': True})

@app.route('/admin/chat/<victim_id>/delete', methods=['POST'])
def delete_chat(victim_id):
    """Delete all messages for a victim"""
    if not is_admin():
        flash('Please login to delete chats', 'warning')
        return redirect(url_for('login'))
    
    delete_chat_messages(victim_id)
    flash('Chat conversation deleted successfully', 'success')
    return redirect(url_for('admin_chat'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# ============================================================================
# FAKE NEWS/MEDIA COVERAGE FEATURE
# ============================================================================

def generate_news_article(victim_id):
    """Generate a realistic fake news article about the victim breach"""
    # Get victim info
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT name, description, sector, ransom_amount, language FROM posts WHERE id = ?', (victim_id,))
    victim = c.fetchone()
    conn.close()
    
    if not victim:
        return None
    
    victim_name = victim['name']
    sector = victim['sector']
    ransom_amount = int(victim['ransom_amount']) if victim['ransom_amount'] else 0
    language = victim['language']
    
    # Language-specific news data
    news_translations = {
        'UK': {
            'publications': [
                'TechNews Daily', 'CyberSecure Weekly', 'Data Breach Report', 
                'Security Intelligence', 'Information Security Review', 
                'DarkWeb Monitor', 'Threat Alert Daily', 'Incident Response News'
            ],
            'authors': [
                'James Mitchell', 'Sarah Chen', 'Robert Davies', 'Emily Thompson',
                'Michael Rodriguez', 'Lisa Anderson', 'David Kumar', 'Alexandra Smith'
            ],
            'impact_statements': {
                'Healthcare': 'Patient privacy breaches could result in HIPAA violations and fines up to $1.5M per violation. Affected individuals may face identity theft.',
                'Finance': 'Potential regulatory investigations by SEC and financial regulators. Investors may face significant losses. Client accounts at risk.',
                'Manufacturing': 'Production lines could remain offline indefinitely. Supply chain disruption could affect multiple industries. Estimated losses in millions.',
                'Retail': 'Customer payment card data exposure violates PCI DSS. Potential credit card fraud affecting thousands of customers.',
                'Technology': 'Proprietary code and trade secrets exposed. Product roadmaps compromised. Competitive disadvantage in market.',
                'Education': 'Student records, financial aid information, and research data compromised. FERPA violations possible.',
                'Government': 'National security implications. Classified or sensitive information potentially disclosed. Public trust severely damaged.',
                'Energy': 'Critical infrastructure vulnerabilities exposed. Operational technology systems at risk. Public safety concerns.',
                'Telecommunications': 'Customer communication records compromised. Network security weaknesses exposed. Regulatory scrutiny expected.',
                'Transportation': 'Logistics and routing information disclosed. Customer travel data at risk. Safety protocols compromised.'
            },
            'expert_quotes': [
                ('Dr. Michael Chen, Chief Security Officer at Global Cyber Institute', 'This is a sophisticated attack targeting critical infrastructure. Organizations must act immediately to secure their systems and notify affected parties.'),
                ('Lisa Rodriguez, Ransomware Threat Analyst', 'This group has demonstrated a pattern of aggressive escalation. Every hour of delay increases the risk of complete data publication.'),
                ('James Park, Incident Response Specialist', 'The scope of this breach suggests systematic access to core business systems. Immediate forensic investigation is critical.'),
                ('Dr. Emily Watson, Cybersecurity Professor', 'This incident highlights the ongoing threat from organized ransomware operations targeting enterprise environments.'),
                ('Marcus Stone, Threat Intelligence Director', 'Intelligence suggests this group has successfully monetized over 200 incidents. Their claims should be taken seriously.')
            ],
            'headline': lambda name, amount, sector: f"{name} Hit by Major Ransomware Attack: ${amount:,} USD Demanded",
            'summary': lambda name, amount, sector: f"{name}, a major {sector.lower()} firm, has fallen victim to a sophisticated ransomware operation. Attackers claim to have exfiltrated sensitive data and are demanding ${amount:,} for its return.",
            'body': lambda name, amount, sector: [
                f"A ransomware gang has publicly claimed responsibility for breaching {name}, a prominent {sector.lower()} organization. According to the attackers, they have successfully exfiltrated sensitive internal data and are threatening its publication on the dark web.",
                f"The group has made an initial ransom demand of ${amount:,} in exchange for the safe deletion of the stolen data. Security researchers confirm the leak site displaying {name}'s information shows signs of a credible threat.",
                "The incident underscores the growing sophistication and brazenness of organized ransomware operations. These groups have evolved from simple encryption attacks to complex operations that combine data exfiltration with public exposure threats.",
                f"Affected parties have been advised to monitor for signs of identity theft and fraudulent activity. Industry experts warn that the {sector.lower()} sector remains a high-value target for cybercriminals.",
                "Preliminary analysis suggests the attackers exploited vulnerabilities in the organization's network perimeter to gain initial access. The attack proceeded undetected for an estimated 2-3 weeks before discovery.",
            ],
            'closing': "As of press time, there has been no official statement from the organization regarding negotiation status or incident response efforts. Regulatory authorities are reportedly reviewing the breach for compliance violations.",
            'source': 'Security Analysis Report',
            'date_format': '%B %d, %Y'
        },
        'FR': {
            'publications': [
                'TechNews Quotidien', 'Cybersécurité Hebdo', 'Rapport sur les Violations',
                'Intelligence en Sécurité', 'Revue de Sécurité Informatique',
                'Moniteur DarkWeb', 'Alerte Quotidienne', 'Nouvelles en Réponse aux Incidents'
            ],
            'authors': [
                'Jean Dubois', 'Marie Leclerc', 'Pierre Bernard', 'Sophie Moreau',
                'Luc Rousseau', 'Anne Dupont', 'Thomas Martin', 'Isabelle Petit'
            ],
            'impact_statements': {
                'Healthcare': 'Les violations de confidentialité pourraient entraîner des violations HIPAA et des amendes jusqu\'à 1,5M$ par violation. Les personnes touchées pourraient faire face à l\'usurpation d\'identité.',
                'Finance': 'Enquêtes réglementaires potentielles par la SEC et les régulateurs financiers. Les investisseurs pourraient subir des pertes importantes. Les comptes des clients sont à risque.',
                'Manufacturing': 'Les lignes de production pourraient rester hors ligne indéfiniment. La perturbation de la chaîne d\'approvisionnement pourrait affecter plusieurs industries.',
                'Retail': 'L\'exposition des données de paiement des clients viole la norme PCI DSS. Fraude par carte de crédit potentielle affectant des milliers de clients.',
                'Technology': 'Code propriétaire et secrets commerciaux exposés. Les feuilles de route des produits compromises. Désavantage compétitif sur le marché.',
                'Education': 'Les dossiers étudiants, les informations d\'aide financière et les données de recherche ont été compromis. Violations possibles de la FERPA.',
                'Government': 'Implications pour la sécurité nationale. Information classifiée ou sensible potentiellement divulguée. Confiance publique gravement endommagée.',
                'Energy': 'Vulnérabilités des infrastructures critiques exposées. Systèmes de technologie opérationnelle à risque. Préoccupations pour la sécurité publique.',
                'Telecommunications': 'Dossiers de communication des clients compromis. Faiblesses de la sécurité réseau exposées. Scrutin réglementaire prévu.',
                'Transportation': 'Informations logistiques et de routage divulguées. Données de voyage des clients à risque. Protocoles de sécurité compromis.'
            },
            'expert_quotes': [
                ('Dr. Michel Chen, Directeur de la Sécurité chez Global Cyber Institute', 'C\'est une attaque sophistiquée ciblant les infrastructures critiques. Les organisations doivent agir immédiatement pour sécuriser leurs systèmes et notifier les parties touchées.'),
                ('Lisa Rodriguez, Analyste en Menaces Ransomware', 'Ce groupe a démontré une tendance à l\'escalade agressive. Chaque heure de retard augmente le risque de publication complète des données.'),
                ('Jacques Parc, Spécialiste en Réponse aux Incidents', 'L\'ampleur de cette violation suggère un accès systématique aux systèmes métier de base. Une enquête médico-légale immédiate est critique.'),
                ('Dr. Émilie Watson, Professeure en Cybersécurité', 'Cet incident met en évidence la menace continue des opérations ransomware organisées ciblant les environnements d\'entreprise.'),
                ('Marc Stone, Directeur de l\'Intelligence sur les Menaces', 'Les services secrets suggèrent que ce groupe a monétisé avec succès plus de 200 incidents. Ses affirmations doivent être prises au sérieux.')
            ],
            'headline': lambda name, amount, sector: f"{name} Victime d\'une Attaque Ransomware Majeure : ${amount:,} USD Demandés",
            'summary': lambda name, amount, sector: f"{name}, une grande entreprise du secteur {sector.lower()}, a été victime d\'une opération ransomware sophistiquée. Les attaquants prétendent avoir exfiltré des données sensibles et exigent ${amount:,} pour leur retour.",
            'body': lambda name, amount, sector: [
                f"Un gang de ransomware a revendiqué publiquement la responsabilité de la violation de {name}, une organisation éminente du secteur {sector.lower()}. Selon les attaquants, ils ont avec succès exfiltré des données internes sensibles et menacent sa publication sur le dark web.",
                f"Le groupe a formulé une demande de rançon initiale de ${amount:,} en échange de la suppression sécurisée des données volées. Les chercheurs en sécurité confirment que le site de fuite affichant les informations de {name} montre des signes de menace crédible.",
                "L\'incident souligne la sophistication croissante et l\'audace des opérations ransomware organisées. Ces groupes ont évolué des simples attaques de chiffrement à des opérations complexes qui combinent l\'exfiltration de données avec des menaces d\'exposition publique.",
                f"Les parties touchées ont été conseillées de surveiller les signes d\'usurpation d\'identité et de fraude. Les experts du secteur avertissent que le secteur {sector.lower()} reste une cible de haute valeur pour les cybercriminels.",
                "L\'analyse préliminaire suggère que les attaquants ont exploité les vulnérabilités du périmètre réseau de l\'organisation pour obtenir un accès initial. L\'attaque a procédé sans être détectée pendant une période estimée de 2-3 semaines avant sa découverte.",
            ],
            'closing': "Au moment de mise sous presse, aucune déclaration officielle de l\'organisation n\'a été faite concernant le statut de négociation ou les efforts de réponse aux incidents. Les autorités de régulation examinant apparemment la violation pour les violations de conformité.",
            'source': 'Rapport d\'Analyse de Sécurité',
            'date_format': '%d %B %Y'
        },
        'DE': {
            'publications': [
                'TechNews Täglich', 'Cybersicherheit Wöchentlich', 'Datenschutzbericht',
                'Sicherheitsintelligenz', 'Informationssicherheitsprüfung',
                'DarkWeb-Monitor', 'Tägliche Bedrohungswarnung', 'Incident Response News'
            ],
            'authors': [
                'Hans Mueller', 'Sophia Schmidt', 'Klaus Weber', 'Maria Braun',
                'Friedrich Hoffmann', 'Gabriele Fischer', 'Wilhelm Schneider', 'Eva Wagner'
            ],
            'impact_statements': {
                'Healthcare': 'Datenschutzverletzungen könnten zu HIPAA-Verstößen und Bußgeldern von bis zu 1,5 Mio. USD pro Verstoß führen. Betroffene könnten Opfer von Identitätsdiebstahl werden.',
                'Finance': 'Mögliche behördliche Untersuchungen durch die SEC und Finanzregulierer. Anleger könnten erhebliche Verluste erleiden. Kundenkonten sind gefährdet.',
                'Manufacturing': 'Produktionslinien könnten auf unbestimmte Zeit offline bleiben. Unterbrechungen der Lieferkette könnten mehrere Industrien beeinflussen.',
                'Retail': 'Die Offenlegung von Zahlungsdaten der Kunden verstößt gegen den PCI-DSS-Standard. Möglicher Kreditkartenbetrug, der Tausende von Kunden betrifft.',
                'Technology': 'Proprietärer Code und Geschäftsgeheimnisse sind exponiert. Produkt-Roadmaps sind kompromittiert. Wettbewerbsnachteil am Markt.',
                'Education': 'Schülerdaten, Informationen zur Studienfinanzierung und Forschungsdaten sind kompromittiert. Mögliche FERPA-Verstöße.',
                'Government': 'Auswirkungen auf die nationale Sicherheit. Möglicherweise Preisgabe von klassifizierten oder sensiblen Informationen. Öffentliches Vertrauen schwer beschädigt.',
                'Energy': 'Schwachstellen der kritischen Infrastruktur sind exponiert. Operationstechnologiesysteme sind gefährdet. Bedenken bezüglich der öffentlichen Sicherheit.',
                'Telecommunications': 'Kommunikationsdatensätze von Kunden sind kompromittiert. Netzwerksicherheitsschwächen sind exponiert. Behördliche Überprüfung wird erwartet.',
                'Transportation': 'Logistik- und Routinginformationen sind offengelegt. Kundereisedaten sind gefährdet. Sicherheitsprotokolle sind kompromittiert.'
            },
            'expert_quotes': [
                ('Dr. Michael Chen, Chief Security Officer bei Global Cyber Institute', 'Dies ist ein ausgefeilter Angriff auf kritische Infrastrukturen. Organisationen müssen sofort handeln, um ihre Systeme zu sichern und betroffene Parteien zu benachrichtigen.'),
                ('Lisa Rodriguez, Ransomware-Bedrohungsanalystin', 'Diese Gruppe hat ein Muster aggressiver Eskalation demonstriert. Jede Stunde Verzögerung erhöht das Risiko der vollständigen Datenveröffentlichung.'),
                ('James Park, Incident-Response-Spezialist', 'Das Ausmaß dieser Verletzung deutet auf systematische Zugriffe auf Kernsysteme hin. Sofortige forensische Untersuchung ist kritisch.'),
                ('Dr. Emily Watson, Professorin für Cybersicherheit', 'Dieser Vorfall unterstreicht die anhaltende Bedrohung durch organisierte Ransomware-Operationen, die Unternehmensumgebungen anvisieren.'),
                ('Marcus Stone, Direktor für Bedrohungserkennung', 'Geheimdienstinformationen deuten darauf hin, dass diese Gruppe über 200 Vorfälle erfolgreich monetarisiert hat. Ihre Behauptungen sollten ernst genommen werden.')
            ],
            'headline': lambda name, amount, sector: f"{name} Opfer großer Ransomware-Attacke: ${amount:,} USD gefordert",
            'summary': lambda name, amount, sector: f"{name}, ein großes Unternehmen im {sector.lower()}-Sektor, ist Opfer einer sophistizierten Ransomware-Operation geworden. Angreifer behaupten, sensible Daten exfiltriert zu haben und fordern ${amount:,} für deren Rückgabe.",
            'body': lambda name, amount, sector: [
                f"Eine Ransomware-Bande hat öffentlich die Verantwortung für die Verletzung von {name}, einer prominenten {sector.lower()}-Organisation, übernommen. Laut den Angreifern haben sie erfolgreich sensible interne Daten exfiltriert und drohen mit deren Veröffentlichung im Dark Web.",
                f"Die Gruppe hat eine anfängliche Lösegeldförderung von ${amount:,} im Austausch gegen die sichere Löschung der gestohlenen Daten gestellt. Sicherheitsforschung bestätigen, dass die Leak-Website, auf der die Informationen von {name} angezeigt werden, Anzeichen einer glaubwürdigen Bedrohung aufweist.",
                "Der Vorfall unterstreicht die wachsende Raffinesse und Dreistigkeit organisierter Ransomware-Operationen. Diese Gruppen haben sich von einfachen Verschlüsselungsangriffen zu komplexen Operationen entwickelt, die Datenexfiltration mit Drohungen zur Offenlegung kombinieren.",
                f"Betroffene Parteien wurden empfohlen, auf Anzeichen von Identitätsdiebstahl und betrügerischer Aktivität zu achten. Branchenexperten warnen, dass der {sector.lower()}-Sektor ein hochwertiges Ziel für Cyberkriminelle bleibt.",
                "Vorläufige Analysen deuten darauf hin, dass Angreifer Schwachstellen im Netzwerkumkreis der Organisation ausgenutzt haben, um anfänglichen Zugriff zu erlangen. Der Angriff verlief unentdeckt für einen geschätzten Zeitraum von 2-3 Wochen vor der Entdeckung.",
            ],
            'closing': "Zum Zeitpunkt der Drucklegung liegt keine offiziellen Stellungnahme der Organisation bezüglich des Verhandlungsstatus oder der Incident-Response-Bemühungen vor. Behörden überprüfen angeblich die Verletzung auf Compliance-Verstöße.",
            'source': 'Sicherheitsanalysebericht',
            'date_format': '%d. %B %Y'
        }
    }
    
    # Get translations for victim's language or default to UK
    translations = news_translations.get(language, news_translations['UK'])
    
    # Select publication and author
    publication = random.choice(translations['publications'])
    author = random.choice(translations['authors'])
    quote_author, quote_text = random.choice(translations['expert_quotes'])
    
    impact = translations['impact_statements'].get(sector, 'Confidential business data exposure poses significant risks.')
    
    # Generate article content using lambda functions
    article_date = datetime.now().strftime(translations['date_format'])
    headline = translations['headline'](victim_name, ransom_amount, sector)
    summary = translations['summary'](victim_name, ransom_amount, sector)
    body = translations['body'](victim_name, ransom_amount, sector)
    closing = translations['closing']
    
    # Related news (simulated) - also in appropriate language
    if language == 'FR':
        related_news = [
            {
                'title': 'Les Attaques Ransomware Augmentent de 40% selon le Dernier Rapport',
                'publication': 'Cybersécurité Hebdo',
                'excerpt': 'Le rapport du secteur montre une augmentation alarmante des campagnes ransomware ciblées contre les organisations d\'entreprise.',
                'url': '#'
            },
            {
                'title': f'Le Secteur {sector} Face à une Targeting Accrue par les Cybercriminels',
                'publication': 'Intelligence en Sécurité',
                'excerpt': f'L\'intelligence sur les menaces indique que les groupes de crime organisé ciblent les cibles à haute valeur du secteur {sector.lower()}.',
                'url': '#'
            },
            {
                'title': 'Les Lois sur la Notification de Violation de Données se Renforcent Mondialement',
                'publication': 'Nouvelles Juridiques Technologiques',
                'excerpt': 'Les nouvelles réglementations exigent une notification plus rapide et pourraient imposer des amendes importantes pour non-conformité.',
                'url': '#'
            }
        ]
    elif language == 'DE':
        related_news = [
            {
                'title': 'Ransomware-Angriffe um 40% in Aktuellem Bericht gestiegen',
                'publication': 'Cybersicherheit Wöchentlich',
                'excerpt': 'Der Branchenbericht zeigt einen alarmierenden Anstieg gezielter Ransomware-Kampagnen gegen Unternehmensorganisationen.',
                'url': '#'
            },
            {
                'title': f'{sector}-Sektor sieht erhöhtes Targeting durch Cyberkriminelle',
                'publication': 'Sicherheitsintelligenz',
                'excerpt': f'Bedrohungsintelligenz zeigt, dass organisierte Kriminalgruppen sich auf hochwertige {sector.lower()}-Ziele konzentrieren.',
                'url': '#'
            },
            {
                'title': 'Datenschutzmitteilungsgesetze weltweit verschärft',
                'publication': 'Legal Tech News',
                'excerpt': 'Neue Vorschriften erfordern schnellere Benachrichtigungen und könnten erhebliche Strafen für Nichteinhaltung vorsehen.',
                'url': '#'
            }
        ]
    else:
        related_news = [
            {
                'title': 'Ransomware Attacks Surge 40% in Latest Threat Report',
                'publication': 'CyberSecure Weekly',
                'excerpt': 'Industry report shows alarming increase in targeted ransomware campaigns against enterprise organizations.',
                'url': '#'
            },
            {
                'title': f'{sector} Sector Faces Increased Targeting by Cybercriminals',
                'publication': 'Security Intelligence',
                'excerpt': f'Threat intelligence indicates organized crime groups focusing on high-value {sector.lower()} targets.',
                'url': '#'
            },
            {
                'title': 'Data Breach Notification Laws Tighten Globally',
                'publication': 'Legal Tech News',
                'excerpt': 'New regulations require faster notification and may impose significant fines for non-compliance.',
                'url': '#'
            }
        ]
    
    return {
        'victim_id': victim_id,
        'victim_name': victim_name,
        'publication': publication,
        'author': author,
        'date': article_date,
        'headline': headline,
        'summary': summary,
        'body': body,
        'impact': impact,
        'quote': quote_text,
        'quote_author': quote_author,
        'quote_source': translations['source'],
        'closing': closing,
        'related_news': related_news
    }

@app.route('/_news/<victim_id>')
def view_news(victim_id):
    """Display fake news article about victim breach"""
    news_article = generate_news_article(victim_id)
    if not news_article:
        return redirect(url_for('index'))
    return render_template('news.html', **news_article)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    init_chat_db()
    
    # Get configuration from environment variables or use defaults
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(debug=debug, port=port)
