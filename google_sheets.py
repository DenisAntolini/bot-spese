import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import matplotlib.pyplot as plt
import tempfile

# Configura l'accesso al foglio Google
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenziali_google.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Spese Familiari").worksheet("Spese")

def registra_movimento(utente, importo, descrizione, tipo):
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([utente, data, importo, descrizione, tipo])

def genera_riepilogo():
    records = sheet.get_all_records()
    riepilogo = {}
    for r in records:
        utente = r['Utente']
        importo = float(r['Importo'])
        tipo = r['Tipo']
        if utente not in riepilogo:
            riepilogo[utente] = 0
        if tipo == "Spesa":
            riepilogo[utente] -= importo
        else:
            riepilogo[utente] += importo

    testo = "Riepilogo saldo per utente:\n"
    for utente, saldo in riepilogo.items():
        testo += f"{utente}: {saldo:.2f}€\n"
    return testo

def genera_grafico():
    import matplotlib.pyplot as plt
    import tempfile

    records = sheet.get_all_records()
    utenti = set(r['Utente'] for r in records)
    dati = {u: 0 for u in utenti}

    for r in records:
        u = r['Utente']
        t = r['Tipo'].strip()
        val = float(r['Importo'])

        if t == 'Spesa':
            dati[u] -= val
        elif t == 'Entrata':
            dati[u] += val

    utenti = list(dati.keys())
    saldi = [dati[u] for u in utenti]

    fig, ax = plt.subplots()
    colori = ['green' if s >= 0 else 'red' for s in saldi]
    ax.bar(utenti, saldi, color=colori)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_ylabel('€')
    ax.set_title('Saldo netto per utente')

    tmpfile = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(tmpfile.name)
    plt.close()
    return tmpfile.name