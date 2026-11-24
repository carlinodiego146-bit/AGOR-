#!/usr/bin/env python3
"""Controlla cards.json prima di ogni pubblicazione.
Uso: python3 strumenti/verifica.py [cards.json]
Esce con codice 1 e un elenco di errori se qualcosa non va: in quel caso NON pubblicare.
"""
import json, re, sys

CATEGORIE = {"storia", "filosofia", "cultura", "mente", "scienza"}
MOTIVI = {
    "atom", "book", "bowl", "cave", "coin", "column", "crown", "cup", "dice", "eye",
    "flag", "flask", "gear", "globe", "head", "helmet", "hourglass", "key", "labyrinth",
    "lamp", "laurel", "letter", "lyre", "mask", "mountain", "owl", "palette", "plane",
    "planet", "pyramid", "quill", "rocket", "satellite", "scales", "scroll", "ship",
    "skull", "sun", "sword", "torch", "tower",
    "brain", "heart", "bulb", "note", "fruit", "fish", "bee", "knight", "dove", "moon",
    "telescope", "map", "compass", "temple", "computer", "chain", "people", "ballot",
    "bolt", "train", "volcano", "mirror", "clock", "dna", "calendar",
}
PREFISSO = {"storia": "s", "filosofia": "f", "cultura": "c", "mente": "m", "scienza": "x"}
CAMPI = {"id", "c", "k", "t", "p", "l", "m", "v", "w", "q"}
LIMITI = {"k": (2, 32), "t": (10, 70), "l": (30, 140)}
IT = {"il", "lo", "gli", "della", "delle", "degli", "che", "è", "sono", "non", "una", "nel", "nella", "per", "con", "alla", "dei", "anche"}
EN = {"the", "of", "and", "to", "in", "was", "is", "a", "it", "that", "were", "for", "on", "with"}


def norm(s):
    return re.sub(r"[^a-z0-9àèéìòù]+", " ", s.lower()).strip()


def controlla(c, dove):
    e = []
    if not isinstance(c, dict) or set(c) != CAMPI:
        return [f"{dove}: i campi devono essere esattamente {sorted(CAMPI)}"]
    if c["c"] not in CATEGORIE:
        e.append(f"{dove}: categoria '{c['c']}' non valida")
    elif not re.fullmatch(PREFISSO[c["c"]] + r"\d{2,3}", str(c["id"])):
        e.append(f"{dove}: id deve essere '{PREFISSO[c['c']]}' + numero")
    for f, (lo, hi) in LIMITI.items():
        if not isinstance(c[f], str) or not lo <= len(c[f]) <= hi:
            e.append(f"{dove}: campo '{f}' lungo {len(str(c[f]))}, ammesso {lo}-{hi}")
    if c["m"] not in MOTIVI:
        e.append(f"{dove}: motivo '{c['m']}' non esiste")
    p = c["p"]
    if not (isinstance(p, list) and 2 <= len(p) <= 4 and all(isinstance(x, str) for x in p)):
        return e + [f"{dove}: 'p' deve avere da 2 a 4 pagine di testo"]
    for i, x in enumerate(p):
        if not 60 <= len(x) <= 260:
            e.append(f"{dove}: pagina {i + 1} lunga {len(x)}, ammesso 60-260")
    testo = " ".join(p)
    if len(testo) > 600:
        e.append(f"{dove}: testo totale lungo {len(testo)}, massimo 600")
    parole = re.findall(r"[a-zà-ù']+", (testo + " " + c["t"]).lower())
    if sum(w in IT for w in parole) >= max(3, sum(w in EN for w in parole)):
        e.append(f"{dove}: il testo sembra italiano, deve essere in inglese")
    v = c["v"]
    if not (isinstance(v, list) and len(v) == len(p) and all(x in MOTIVI for x in v)):
        e.append(f"{dove}: 'v' deve avere un motivo valido per ogni pagina ({len(p)})")
    w = c["w"]
    if not (isinstance(w, list) and 2 <= len(w) <= 4):
        e.append(f"{dove}: 'w' deve avere da 2 a 4 parole")
    else:
        visti = set()
        for x in w:
            if not (isinstance(x, list) and len(x) == 2 and all(isinstance(y, str) and 1 <= len(y) <= 40 for y in x)):
                e.append(f"{dove}: ogni parola di 'w' è [inglese, italiano]")
                continue
            if x[0].lower() in visti:
                e.append(f"{dove}: parola '{x[0]}' ripetuta")
            visti.add(x[0].lower())
            if not re.search(r"(?<![\w])" + re.escape(x[0]) + r"(?![\w])", testo, re.I):
                e.append(f"{dove}: la parola '{x[0]}' non compare nel testo delle pagine")
    q = c["q"]
    if not (isinstance(q, list) and len(q) == 4 and all(isinstance(x, str) and 1 <= len(x) <= 100 for x in q)):
        e.append(f"{dove}: 'q' deve essere [domanda, giusta, sbagliata, sbagliata], max 100 caratteri")
    elif len({norm(x) for x in q[1:]}) != 3:
        e.append(f"{dove}: risposte del quiz non distinte")
    return e


def main(path):
    try:
        testo = open(path, encoding="utf-8").read()
        dati = json.loads(testo)
    except Exception as ex:
        print(f"ERRORE: JSON non valido: {ex}")
        return 1
    if not isinstance(dati, list) or not dati:
        print("ERRORE: il file deve essere una lista non vuota")
        return 1
    errori, ids, titoli = [], set(), {}
    for i, c in enumerate(dati):
        dove = f"scheda {i} ({c.get('id', '?') if isinstance(c, dict) else '?'})"
        errori += controlla(c, dove)
        if isinstance(c, dict):
            if c.get("id") in ids:
                errori.append(f"{dove}: id duplicato")
            ids.add(c.get("id"))
            t = norm(str(c.get("t", "")))
            if t in titoli:
                errori.append(f"{dove}: titolo uguale a {titoli[t]}")
            titoli[t] = c.get("id")
    righe = [l for l in testo.strip().splitlines() if l not in ("[", "]")]
    if len(righe) != len(dati):
        errori.append("formato: una scheda per riga, tra '[' e ']' su righe proprie")
    if errori:
        print("\n".join("ERRORE: " + e for e in errori))
        return 1
    conta = {k: sum(1 for c in dati if c["c"] == k) for k in sorted(CATEGORIE)}
    print(f"OK: {len(dati)} schede", conta)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "cards.json"))
