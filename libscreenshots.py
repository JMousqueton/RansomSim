"""Generate fake screenshot images for proof of breach gallery"""
import random
from datetime import datetime, timedelta


def generate_database_screenshot(language='UK'):
    """Generate SVG screenshot of database export"""
    rows = []
    
    # Country-specific names (20+ per country)
    names_by_country = {
        'UK': ["Oliver Thompson", "Emma Watson", "George Williams", "Charlotte Davies", "Harry Brown", 
               "Sophie Taylor", "Jack Wilson", "Amelia Roberts", "Thomas Moore", "Emily Clark",
               "Alexander Grant", "Isabella Foster", "Benjamin Pritchard", "Mia Richardson", "Lucas Jenkins",
               "Harper Davies", "Ethan Marshall", "Evelyn Stone", "Mason Cooper", "Abigail Brooks"],
        'FR': ["Pierre Dubois", "Marie Martin", "Jean Bernard", "Sophie Petit", "Luc Moreau",
               "Camille Laurent", "Antoine Leroy", "Chloé Simon", "Nicolas Lefebvre", "Julie Bonnet",
               "François Gérard", "Amélie Renaud", "Maxime Fontaine", "Océane Blanc", "Sébastien Roux",
               "Léa Guerin", "Paul Delorme", "Audrey Arnould", "Romain Collet", "Viviane Jolivet"],
        'DE': ["Lukas Müller", "Emma Schmidt", "Felix Weber", "Sophie Schneider", "Max Fischer",
               "Anna Meyer", "Leon Wagner", "Mia Becker", "Paul Hoffmann", "Laura Schulz",
               "Tobias Krämer", "Hannah Richter", "Julian Reiter", "Sophia König", "David Neumann",
               "Lena Baumann", "Markus Pfeiffer", "Jana Strauss", "Simon Hartmann", "Clara Stein"]
    }
    
    names = names_by_country.get(language, names_by_country['UK'])
    
    # Country-specific email domains
    domains_by_country = {
        'UK': ['yahoo.co.uk', 'btopenworld.com', 'hotmail.co.uk', 'ntlworld.com', 'btinternet.com'],
        'FR': ['yahoo.fr', 'free.fr', 'wanadoo.fr', 'orange.fr', 'sfr.fr'],
        'DE': ['web.de', 'gmx.de', 't-online.de', 'freenet.de', 'arcor.de']
    }
    domains = domains_by_country.get(language, domains_by_country['UK'])
    
    # Currency symbol by country
    currency = '£' if language == 'UK' else '€'
    
    for i in range(8):
        name = random.choice(names)
        domain = random.choice(domains)
        email = f"{name.lower().replace('ö','o').replace('ü','u').replace(' ', '.')}@{domain}"
        salary = random.randint(45000, 150000)
        
        # Country-specific ID formats
        if language == 'FR':
            # INSEE number format: 13 digits
            id_number = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            formatted_id = f"{id_number[:2]} {id_number[2:4]} {id_number[4:6]} {id_number[6:9]} {id_number[9:13]}"
        elif language == 'DE':
            # Personalausweisnummer format: 10 digits
            id_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            formatted_id = f"{id_number[:2]} {id_number[2:5]} {id_number[5:8]} {id_number[8:10]}"
        else:  # UK
            # National Insurance Number format: 2 letters + 6 digits + 1 letter
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            formatted_id = f"{random.choice(letters)}{random.choice(letters)}{random.randint(100000, 999999)}{random.choice(letters)}"
        
        rows.append(f'<text x="10" y="{100 + i*25}" font-size="11" fill="#e5e7eb" font-family="Courier New">{i+1:3d} | {name:20s} | {email:30s} | {currency}{salary:,} | {formatted_id}</text>')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
  <defs>
    <linearGradient id="dbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1f2937;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#111827;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="450" fill="url(#dbGrad)"/>
  
  <!-- Terminal header -->
  <rect x="0" y="0" width="800" height="40" fill="#0f172a"/>
  <circle cx="20" cy="20" r="6" fill="#ef4444"/>
  <circle cx="40" cy="20" r="6" fill="#eab308"/>
  <circle cx="60" cy="20" r="6" fill="#22c55e"/>
  <text x="90" y="25" font-size="14" fill="#94a3b8" font-family="monospace">employees_export.csv - 18,420 records</text>
  
  <!-- Header -->
  <text x="10" y="70" font-size="12" fill="#10b981" font-weight="bold" font-family="Courier New">ID  | NAME                 | EMAIL                          | SALARY   | SSN</text>
  <line x1="10" y1="75" x2="790" y2="75" stroke="#374151" stroke-width="1"/>
  
  <!-- Data rows -->
  {chr(10).join(rows)}
  
  <!-- Warning footer -->
  <rect x="0" y="410" width="800" height="40" fill="#7f1d1d" opacity="0.9"/>
  <text x="20" y="435" font-size="13" fill="#fca5a5" font-family="sans-serif">⚠ CONFIDENTIAL - PII DATA EXPOSED</text>
  <text x="680" y="435" font-size="11" fill="#fca5a5" font-family="monospace">18.4k rows</text>
</svg>'''
    return svg


def generate_legal_screenshot(language='UK'):
    """Generate SVG screenshot of legal document"""
    date = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%B %d, %Y")
    
    # Country-specific NDA text
    if language == 'FR':
        title = "ACCORD DE CONFIDENTIALITÉ"
        stamp_text = "CONFIDENTIEL"
        stamp_subtext = "USAGE INTERNE"
        date_label = "Date:"
        classification = "Classification: STRICTEMENT CONFIDENTIEL"
        parties_title = "PARTIES À CET ACCORD"
        party1 = "1. [NOM DE L'ENTREPRISE] (\"Partie Divulgatrice\")"
        party2 = "2. [REDACTÉ] (\"Partie Recevante\")"
        ma_title = "DISCUSSIONS FUSION &amp; ACQUISITION"
        ma_text = "Cet accord couvre les informations confidentielles concernant:"
        bullet1 = "&#8226; Évaluation de la cible d'acquisition stratégique (évaluation €███M)"
        bullet2 = "&#8226; Projections financières et prévisions de revenus (FY 2024-2026)"
        bullet3 = "&#8226; Documentation d'approbation du conseil et registres de vote"
        bullet4 = "&#8226; Packages de rétention des salariés et indemnités de départ"
        bullet5 = "&#8226; Portefeuille IP et accords de licence de brevets"
        conf_title = "OBLIGATIONS DE CONFIDENTIALITÉ"
        conf_text1 = "La Partie Recevante s'engage à ne pas divulguer d'informations confidentielles"
        conf_text2 = "aux tiers sans consentement écrit préalable. Pénalités: €5M."
        sig_label = "Signature Autorisée: ___[REDACTÉ]___"
        warning = "&#9888; VIOLATION DU NDA - DIVULGATION NON AUTORISÉE"
    elif language == 'DE':
        title = "GEHEIMHALTUNGSVEREINBARUNG"
        stamp_text = "VERTRAULICH"
        stamp_subtext = "INTERNE VERWENDUNG"
        date_label = "Datum:"
        classification = "Klassifizierung: STRENG VERTRAULICH"
        parties_title = "PARTEIEN DIESER VEREINBARUNG"
        party1 = "1. [FIRMENNAME] (\"Offenbarende Partei\")"
        party2 = "2. [REDACTED] (\"Empfangende Partei\")"
        ma_title = "DISKUSSIONEN FUSION &amp; ÜBERNAHME"
        ma_text = "Diese Vereinbarung deckt vertrauliche Informationen bezüglich:"
        bullet1 = "&#8226; Bewertung des strategischen Übernahmeziels (€███M Bewertung)"
        bullet2 = "&#8226; Finanzielle Prognosen und Umsatzprognosen (FJ 2024-2026)"
        bullet3 = "&#8226; Genehmigungsdokumentation und Abstimmungsunterlagen des Vorstands"
        bullet4 = "&#8226; Mitarbeiterbindungs- und Abfindungspakete"
        bullet5 = "&#8226; IP-Portfolio und Patentlizenzvereinbarungen"
        conf_title = "VERTRAULICHKEITSVERPFLICHTUNGEN"
        conf_text1 = "Die empfangende Partei erklärt sich bereit, vertrauliche Informationen"
        conf_text2 = "nicht an Dritte weiterzugeben ohne vorherige schriftliche Zustimmung. Strafgelder: €5M."
        sig_label = "Autorisierte Unterschrift: ___[REDACTED]___"
        warning = "&#9888; VERLETZUNG DER GEHEIMHALTUNGSVEREINBARUNG - UNBEFUGTE OFFENBARUNG"
    else:  # UK
        title = "NON-DISCLOSURE AGREEMENT"
        stamp_text = "CONFIDENTIAL"
        stamp_subtext = "INTERNAL USE"
        date_label = "Date:"
        classification = "Classification: STRICTLY CONFIDENTIAL"
        parties_title = "PARTIES TO THIS AGREEMENT"
        party1 = "1. [COMPANY NAME] (\"Disclosing Party\")"
        party2 = "2. [REDACTED] (\"Receiving Party\")"
        ma_title = "MERGER &amp; ACQUISITION DISCUSSIONS"
        ma_text = "This agreement covers confidential information regarding:"
        bullet1 = "&#8226; Strategic acquisition target evaluation ($███M valuation)"
        bullet2 = "&#8226; Financial projections and revenue forecasts (FY 2024-2026)"
        bullet3 = "&#8226; Board approval documentation and voting records"
        bullet4 = "&#8226; Employee retention and severance packages"
        bullet5 = "&#8226; IP portfolio and patent licensing agreements"
        conf_title = "CONFIDENTIALITY OBLIGATIONS"
        conf_text1 = "The Receiving Party agrees not to disclose any confidential information"
        conf_text2 = "to third parties without prior written consent. Breach penalties: $5M."
        sig_label = "Authorized Signature: ___[REDACTED]___"
        warning = "&#9888; BREACH OF NDA - UNAUTHORIZED DISCLOSURE"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
  <defs>
    <linearGradient id="legalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0ea5e9;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#312e81;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="450" fill="url(#legalGrad)"/>
  
  <!-- Document container -->
  <rect x="100" y="40" width="600" height="370" fill="#ffffff" rx="4"/>
  
  <!-- Header -->
  <rect x="100" y="40" width="600" height="50" fill="#1e40af" rx="4" ry="4"/>
  <text x="400" y="72" font-size="18" fill="#ffffff" font-weight="bold" text-anchor="middle" font-family="serif">{title}</text>
  
  <!-- Stamp -->
  <circle cx="620" cy="140" r="30" fill="none" stroke="#dc2626" stroke-width="2.5" opacity="0.8"/>
  <text x="620" y="136" font-size="9" fill="#dc2626" font-weight="bold" text-anchor="middle" font-family="sans-serif">{stamp_text}</text>
  <text x="620" y="147" font-size="7" fill="#dc2626" text-anchor="middle" font-family="sans-serif">{stamp_subtext}</text>
  
  <!-- Content -->
  <text x="130" y="120" font-size="10" fill="#374151" font-family="serif">{date_label} {date}</text>
  <text x="130" y="138" font-size="10" fill="#374151" font-family="serif">{classification}</text>
  
  <text x="130" y="170" font-size="11" fill="#111827" font-weight="bold" font-family="serif">{parties_title}</text>
  <text x="130" y="188" font-size="9" fill="#4b5563" font-family="serif">{party1}</text>
  <text x="130" y="202" font-size="9" fill="#4b5563" font-family="serif">{party2}</text>
  
  <text x="130" y="230" font-size="11" fill="#111827" font-weight="bold" font-family="serif">{ma_title}</text>
  <text x="130" y="248" font-size="9" fill="#4b5563" font-family="serif">{ma_text}</text>
  <text x="150" y="262" font-size="8" fill="#6b7280" font-family="serif">{bullet1}</text>
  <text x="150" y="275" font-size="8" fill="#6b7280" font-family="serif">{bullet2}</text>
  <text x="150" y="288" font-size="8" fill="#6b7280" font-family="serif">{bullet3}</text>
  <text x="150" y="301" font-size="8" fill="#6b7280" font-family="serif">{bullet4}</text>
  <text x="150" y="314" font-size="8" fill="#6b7280" font-family="serif">{bullet5}</text>
  
  <text x="130" y="340" font-size="11" fill="#111827" font-weight="bold" font-family="serif">{conf_title}</text>
  <text x="130" y="356" font-size="8" fill="#4b5563" font-family="serif">{conf_text1}</text>
  <text x="130" y="368" font-size="8" fill="#4b5563" font-family="serif">{conf_text2}</text>
  
  <line x1="130" y1="385" x2="500" y2="385" stroke="#d1d5db" stroke-width="1"/>
  <text x="130" y="398" font-size="7" fill="#9ca3af" font-family="sans-serif">{sig_label}</text>
  <text x="380" y="398" font-size="7" fill="#9ca3af" font-family="sans-serif">{date_label} {date}</text>
  
  <!-- Warning -->
  <rect x="0" y="420" width="800" height="30" fill="#991b1b" opacity="0.95"/>
  <text x="400" y="440" font-size="12" fill="#fecaca" font-weight="bold" text-anchor="middle" font-family="sans-serif">{warning}</text>
</svg>'''
    return svg


def generate_email_screenshot(language='UK'):
    """Generate SVG screenshot of Outlook email inbox"""
    
    # Country-specific email subjects and senders
    if language == 'FR':
        subjects = [
            ("Plan de Restructuration Q4 - CONFIDENTIEL", "Bureau du PDG", "14:32", True),
            ("RE: Litige Contrat Fournisseur - Juridique", "Service Juridique", "12/15", False),
            ("URGENT: Réponse Incident Sécurité", "RSSI", "Hier", True),
            ("TR: Liste Licenciements - NE PAS PARTAGER", "Directeur RH", "12/10", True),
            ("Aperçu Résultats Financiers (Pré-publication)", "DAF", "12/08", False),
            ("TR: Analyse Cible F&amp;A - Revue Conseil", "VP Stratégie", "12/05", True),
        ]
    elif language == 'DE':
        subjects = [
            ("Q4-Umstrukturierungsplan - VERTRAULICH", "CEO-Büro", "14:32", True),
            ("RE: Lieferantenvertragsstreit - Recht", "Rechtsabteilung", "12/15", False),
            ("DRINGEND: Sicherheitsvorfallreaktion", "CISO", "Gestern", True),
            ("WG: Kündigungsliste - NICHT TEILEN", "HR-Direktor", "12/10", True),
            ("Finanzergebnisvorschau (Vor Veröffentlichung)", "CFO", "12/08", False),
            ("WG: M&amp;A-Zielanalyse - Vorstandsprüfung", "VP Strategie", "12/05", True),
        ]
    else:  # UK
        subjects = [
            ("Q4 Restructuring Plan - CONFIDENTIAL", "CEO Office", "14:32", True),
            ("RE: Vendor Contract Dispute - Legal", "Legal Department", "12/15", False),
            ("URGENT: Security Incident Response", "CISO", "Yesterday", True),
            ("FW: Employee Termination List - DO NOT SHARE", "HR Director", "12/10", True),
            ("Financial Results Preview (Pre-Earnings)", "CFO", "12/08", False),
            ("M&amp;A Target Analysis - Board Review", "Strategy VP", "12/05", True),
        ]
    
    email_rows = []
    y_pos = 145
    for i, (subject, sender, date, unread) in enumerate(subjects):
        bg_color = "#f3f4f6" if i % 2 == 0 else "#ffffff"
        font_weight = "bold" if unread else "normal"
        unread_indicator = '<circle cx="70" cy="{}" r="4" fill="#0078d4"/>'.format(y_pos + 15) if unread else ''
        
        email_rows.append(f'''
  <rect x="60" y="{y_pos}" width="740" height="32" fill="{bg_color}"/>
  {unread_indicator}
  <text x="85" y="{y_pos + 12}" font-size="10" fill="#323130" font-weight="{font_weight}" font-family="Arial, sans-serif">{sender}</text>
  <text x="85" y="{y_pos + 24}" font-size="9" fill="#605e5c" font-family="Arial, sans-serif">{subject}</text>
  <text x="750" y="{y_pos + 18}" font-size="9" fill="#605e5c" font-family="Arial, sans-serif" text-anchor="end">{date}</text>''')
        y_pos += 33
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
  <!-- Background -->
  <rect width="800" height="450" fill="#faf9f8"/>
  
  <!-- Top navigation bar -->
  <rect x="0" y="0" width="800" height="48" fill="#0078d4"/>
  <text x="15" y="30" font-size="16" fill="#ffffff" font-weight="600" font-family="Arial, sans-serif">Outlook</text>
  <rect x="100" y="10" width="200" height="28" fill="#106ebe" rx="2"/>
  <text x="110" y="30" font-size="12" fill="#ffffff" font-family="Arial, sans-serif">Search emails...</text>
  
  <!-- Command bar -->
  <rect x="0" y="48" width="800" height="40" fill="#f3f2f1"/>
  <g transform="translate(15, 60)">
    <rect width="60" height="24" fill="#0078d4" rx="2"/>
    <text x="30" y="16" font-size="11" fill="#ffffff" text-anchor="middle" font-family="Arial, sans-serif">New</text>
  </g>
  <text x="90" y="76" font-size="11" fill="#323130" font-family="Arial, sans-serif">Delete</text>
  <text x="140" y="76" font-size="11" fill="#323130" font-family="Arial, sans-serif">Archive</text>
  <text x="195" y="76" font-size="11" fill="#323130" font-family="Arial, sans-serif">Move to</text>
  <text x="250" y="76" font-size="11" fill="#323130" font-family="Arial, sans-serif">Categories</text>
  
  <!-- Folder pane -->
  <rect x="0" y="88" width="60" height="362" fill="#f3f2f1"/>
  <rect x="15" y="100" width="30" height="25" fill="#0078d4" rx="2"/>
  <text x="30" y="117" font-size="12" fill="#ffffff" text-anchor="middle" font-family="Arial, sans-serif">&#128194;</text>
  <rect x="15" y="140" width="30" height="25" fill="#605e5c" rx="2"/>
  <text x="30" y="157" font-size="12" fill="#ffffff" text-anchor="middle" font-family="Arial, sans-serif">&#9993;</text>
  <rect x="15" y="180" width="30" height="25" fill="#605e5c" rx="2"/>
  <text x="30" y="197" font-size="12" fill="#ffffff" text-anchor="middle" font-family="Arial, sans-serif">&#128228;</text>
  
  <!-- Email list header -->
  <rect x="60" y="88" width="740" height="55" fill="#ffffff"/>
  <text x="70" y="110" font-size="16" fill="#323130" font-weight="600" font-family="Arial, sans-serif">Inbox</text>
  <text x="70" y="130" font-size="11" fill="#605e5c" font-family="Arial, sans-serif">Filtered by: All &#8226; Sort: Date &#9660;</text>
  <rect x="720" y="100" width="70" height="24" fill="#edebe9" rx="2"/>
  <text x="755" y="116" font-size="10" fill="#323130" text-anchor="middle" font-family="Arial, sans-serif">Filter &#9660;</text>
  
  <!-- Email list -->
  {''.join(email_rows)}
  
  <!-- Status bar -->
  <rect x="0" y="420" width="800" height="30" fill="#323130"/>
  <text x="15" y="440" font-size="10" fill="#ffffff" font-family="Arial, sans-serif">Total: 2,847 items | Unread: 47 | Selected: 0</text>
  <rect x="680" y="427" width="110" height="18" fill="#d13438" rx="2"/>
  <text x="735" y="439" font-size="9" fill="#ffffff" font-weight="bold" text-anchor="middle" font-family="Arial, sans-serif">&#9888; EXFILTRATED</text>
</svg>'''
    return svg
