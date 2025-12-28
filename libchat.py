import sqlite3
from datetime import datetime

KEYWORDS = {
    'proof': ['proof', 'sample', 'decrypt', 'demonstration', 'evidence', 'verify'],
    'negotiate': ['price', 'discount', 'lower', 'negotiate', 'offer', 'counter', 'amount', 'expensive'],
    'deadline': ['deadline', 'extension', 'time', 'delay', 'postpone', 'extend'],
    'law': ['police', 'law', 'authority', 'court', 'legal', 'fbi', 'interpol'],
    'payment': ['bitcoin', 'crypto', 'cryptocurrency', 'payment', 'transfer', 'wallet', 'monero'],
    'contact': ['contact', 'phone', 'email', 'message', 'reach', 'communicate'],
    'recovery': ['recover', 'restore', 'backup', 'recovery', 'decryption tool'],
    'publish': ['publish', 'release', 'leak', 'expose', 'public', 'media'],
    'threat': ['threat', 'report', 'authorities', 'shut down', 'stop', 'compliance'],
}


def _get_victim_info(victim_id):
    conn = sqlite3.connect('ransomsim.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT name, ransom_amount, deadline_date, language, auto_respond FROM posts WHERE id = ?', (victim_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {}


def _get_chat_history(victim_id):
    conn = sqlite3.connect('ransomsim-chat.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT sender, message, created_at FROM messages WHERE victim_id = ? ORDER BY created_at ASC', (victim_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _has_gang_message(history):
    return any(msg['sender'] == 'gang' for msg in history)


def _normalize(text):
    return (text or '').lower().strip()


def _contains_any(text, words):
    t = _normalize(text)
    return any(w in t for w in words)


def _format_deadline(deadline):
    if not deadline:
        return None
    try:
        # Stored format 'YYYY-MM-DD HH:MM:SS'
        return datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M UTC')
    except Exception:
        return deadline


def generate_auto_response(victim_id: str, message: str) -> str:
    """Return an automated gang response based on the victim message and chat state.
    Empty string means no auto-response (either disabled or should not reply).
    """
    info = _get_victim_info(victim_id)
    
    # Check if auto-respond is disabled for this victim
    if info.get('auto_respond') != '1':
        return ''
    
    history = _get_chat_history(victim_id)
    victim_msg = _normalize(message)

    ransom = info.get('ransom_amount') or '500000'
    deadline = _format_deadline(info.get('deadline_date'))

    # First contact: send initial demand if gang hasn't spoken yet
    if not _has_gang_message(history):
        parts = [
            f"We control your network and your confidential data.",
            f"The demand is ${ransom}. Payment in cryptocurrency only (Bitcoin/Monero preferred).",
        ]
        if deadline:
            parts.append(f"Deadline: {deadline}. After this, we publish and sell your data.")
        parts.append("Reply here to negotiate or request proof of decryption.")
        return "\n".join(parts)

    # Proof / sample decryption
    if _contains_any(victim_msg, KEYWORDS['proof']):
        return (
            "We will decrypt a small sample (max 3 files <5MB total) to prove capability.\n"
            "Send the file names you want as proof. We will return 1 sample within 24 hours.\n"
            "This does not change the demand or the deadline.\n"
            "Proof files are non-negotiable and part of the recovery process."
        )

    # Payment / Cryptocurrency methods
    if _contains_any(victim_msg, KEYWORDS['payment']):
        return (
            "Accepted payment methods:\n"
            "- Bitcoin (BTC): Single address per victim\n"
            "- Monero (XMR): Preferred for privacy\n"
            "Minimum payment: 0.5 BTC equivalent\n"
            "After payment confirmation, decryption key will be delivered within 1 hour.\n"
            "No chargeback possible with crypto. Payment is final."
        )

    # Negotiation / price discussions
    if _contains_any(victim_msg, KEYWORDS['negotiate']):
        return (
            f"Limited discounts available:\n"
            f"- 10% reduction if paid within 24 hours: ${int(ransom) * 0.9}\n"
            f"- No negotiation after deadline. Price increases to ${int(ransom) * 1.5}.\n"
            f"Current demand is fair for the data volume we hold.\n"
            f"Delays increase exposure and likelihood of publication."
        )

    # Deadline / extension requests
    if _contains_any(victim_msg, KEYWORDS['deadline']):
        ext_line = "Extensions cost 10% of the base ransom per 24 hours.\n"
        if deadline:
            ext_line += f"Current deadline: {deadline}.\n"
        return (
            ext_line + 
            "Further delays guarantee publication on the public leak site.\n"
            "Every hour you delay, more potential buyers gain access to your data."
        )

    # Law enforcement / authority threats
    if _contains_any(victim_msg, KEYWORDS['law']):
        return (
            "Do not contact law enforcement or third-party recovery services.\n"
            "Authorities cannot decrypt our encryption.\n"
            "Attempts to involve authorities will trigger immediate publication.\n"
            "We monitor communications. Betrayal has consequences.\n"
            "Pay or lose everything—it's your choice."
        )

    # Contact / communication methods
    if _contains_any(victim_msg, KEYWORDS['contact']):
        return (
            "This chat is your ONLY secure communication channel.\n"
            "Do not attempt to contact us via other means.\n"
            "Phone calls, emails, or third-party intermediaries will be ignored.\n"
            "Respond here with serious negotiation or payment instructions."
        )

    # Data recovery / backup mention
    if _contains_any(victim_msg, KEYWORDS['recovery']):
        return (
            "Your backups are encrypted too. We found them all.\n"
            "Recovery software, tools, and paid services cannot help.\n"
            "Only our decryption key will restore your data.\n"
            "Stop wasting time. Pay and get back online."
        )

    # Publication / leak threats
    if _contains_any(victim_msg, KEYWORDS['publish']):
        parts = [
            "Yes, we WILL publish your data if you don't pay.",
            "Our buyers are competitors, journalists, and interested parties.",
            "Your data is valuable. We have multiple buyers already lined up.",
        ]
        if deadline:
            parts.append(f"Publication begins immediately after {deadline}.")
        parts.append("The longer you delay, the more copies spread. Act now.")
        return "\n".join(parts)

    # Threats or confrontational messages
    if _contains_any(victim_msg, KEYWORDS['threat']):
        return (
            "We appreciate your boldness, but threats won't work here.\n"
            "We operate from jurisdictions beyond reach.\n"
            "You have one option: pay or lose your data.\n"
            "We've done this thousands of times. You won't be the first to pay.\n"
            "The clock is ticking."
        )

    # Default: remind of demand and deadline
    default_lines = [
        f"Payment demand remains ${ransom}.",
        "We expect a serious offer or prompt payment.",
    ]
    if deadline:
        default_lines.append(f"Deadline: {deadline}. Time is running out.")
    default_lines.append("Ask for a sample, propose terms, or arrange payment.")
    return "\n".join(default_lines)
