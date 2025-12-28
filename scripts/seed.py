#!/usr/bin/env python3
import os
import sqlite3
import random
import string
from datetime import datetime, timedelta, timezone
from faker import Faker

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'ransomsim.db')

SECTORS = [
    'healthcare','finance','manufacturing','retail','technology',
    'education','government','energy','telecommunications','transportation'
]
LANGUAGES = ['UK','FR','DE']

fake_locales = {
    'UK': Faker('en_GB'),
    'FR': Faker('fr_FR'),
    'DE': Faker('de_DE')
}


def generate_random_id(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def ensure_db():
    conn = sqlite3.connect(DB_PATH)
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
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


def make_documents(language, count):
    # Simple placeholder docs using Faker; app generates detailed names at runtime
    locale = fake_locales.get(language, fake_locales['UK'])
    docs = []
    for _ in range(count):
        docs.append(locale.file_name(extension=random.choice(['pdf','xlsx','docx'])))
    return docs


def make_files(language, count):
    locale = fake_locales.get(language, fake_locales['UK'])
    files = []
    for _ in range(count):
        prefix = locale.word()
        suffix = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        ts = random.randint(20200101, 20251231)
        ext = random.choice(['xlsx','docx','pdf'])
        files.append(f"{prefix}_{suffix}_{ts}.{ext}")
    return files


def seed_one(conn, idx):
    language = random.choice(LANGUAGES)
    locale = fake_locales[language]
    post_id = generate_random_id()
    name = locale.company()
    description = locale.text(max_nb_chars=200)
    sector = random.choice(SECTORS)
    ransom_amount = str(random.choice([100000,250000,500000,750000,1000000,2000000]))
    # Deadline within next 3 to 7 days (UTC, timezone-aware)
    deadline = (datetime.now(timezone.utc) + timedelta(days=random.randint(3,7), hours=random.randint(0,23))).strftime('%Y-%m-%d %H:%M:%S')

    document_names = make_documents(language, random.randint(10,15))
    file_names = make_files(language, random.randint(10,15))

    c = conn.cursor()
    c.execute('''INSERT INTO posts (id, name, logo_path, description, language, document_names, file_names, sector, ransom_amount, deadline_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (post_id, name, None, description, language, ','.join(document_names), ','.join(file_names), sector, ransom_amount, deadline))
    conn.commit()
    return post_id


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Seed RansomSim database with fake victims')
    parser.add_argument('-n', '--num', type=int, default=10, help='Number of victims to create')
    args = parser.parse_args()

    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    created = []
    for i in range(args.num):
        created.append(seed_one(conn, i+1))
    conn.close()

    print(f"Seeded {len(created)} victims. Example IDs:")
    for pid in created[:5]:
        print(f" - {pid}")

if __name__ == '__main__':
    main()
