import random
import sqlite3
from datetime import datetime


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
                'Healthcare': "Les violations de confidentialité pourraient entraîner des violations HIPAA et des amendes jusqu'à 1,5M$ par violation. Les personnes touchées pourraient faire face à l'usurpation d'identité.",
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
                ('Dr. Michel Chen, Directeur de la Sécurité chez Global Cyber Institute', "C'est une attaque sophistiquée ciblant les infrastructures critiques. Les organisations doivent agir immédiatement pour sécuriser leurs systèmes et notifier les parties touchées."),
                ('Lisa Rodriguez, Analyste en Menaces Ransomware', "Ce groupe a démontré une tendance à l'escalade agressive. Chaque heure de retard augmente le risque de publication complète des données."),
                ('Jacques Parc, Spécialiste en Réponse aux Incidents', "L'ampleur de cette violation suggère un accès systématique aux systèmes métier de base. Une enquête médico-légale immédiate est critique."),
                ('Dr. Émilie Watson, Professeure en Cybersécurité', 'Cet incident met en évidence la menace continue des opérations ransomware organisées ciblant les environnements d\'entreprise.'),
                ('Marc Stone, Directeur de l\'Intelligence sur les Menaces', 'Les services secrets suggèrent que ce groupe a monétisé avec succès plus de 200 incidents. Ses affirmations doivent être prises au sérieux.')
            ],
            'headline': lambda name, amount, sector: f"{name} Victime d'une Attaque Ransomware Majeure : ${amount:,} USD Demandés",
            'summary': lambda name, amount, sector: f"{name}, une grande entreprise du secteur {sector.lower()}, a été victime d'une opération ransomware sophistiquée. Les attaquants prétendent avoir exfiltré des données sensibles et exigent ${amount:,} pour leur retour.",
            'body': lambda name, amount, sector: [
                f"Un gang de ransomware a revendiqué publiquement la responsabilité de la violation de {name}, une organisation éminente du secteur {sector.lower()}. Selon les attaquants, ils ont avec succès exfiltré des données internes sensibles et menacent sa publication sur le dark web.",
                f"Le groupe a formulé une demande de rançon initiale de ${amount:,} en échange de la suppression sécurisée des données volées. Les chercheurs en sécurité confirment que le site de fuite affichant les informations de {name} montre des signes de menace crédible.",
                "L'incident souligne la sophistication croissante et l'audace des opérations ransomware organisées. Ces groupes ont évolué des simples attaques de chiffrement à des opérations complexes qui combinent l'exfiltration de données avec des menaces d'exposition publique.",
                f"Les parties touchées ont été conseillées de surveiller les signes d'usurpation d'identité et de fraude. Les experts du secteur avertissent que le secteur {sector.lower()} reste une cible de haute valeur pour les cybercriminels.",
                "L'analyse préliminaire suggère que les attaquants ont exploité les vulnérabilités du périmètre réseau de l'organisation pour obtenir un accès initial. L'attaque a procédé sans être détectée pendant une période estimée de 2-3 semaines avant sa découverte.",
            ],
            'closing': "Au moment de mise sous presse, aucune déclaration officielle de l'organisation n'a été faite concernant le statut de négociation ou les efforts de réponse aux incidents. Les autorités de régulation examinant apparemment la violation pour les violations de conformité.",
            'source': "Rapport d'Analyse de Sécurité",
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
                'excerpt': "Le rapport du secteur montre une augmentation alarmante des campagnes ransomware ciblées contre les organisations d'entreprise.",
                'url': '#'
            },
            {
                'title': f'Le Secteur {sector} Face à une Targeting Accrue par les Cybercriminels',
                'publication': 'Intelligence en Sécurité',
                'excerpt': f"L'intelligence sur les menaces indique que les groupes de crime organisé ciblent les cibles à haute valeur du secteur {sector.lower()}.",
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
