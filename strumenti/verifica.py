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
}
PREFISSO = {"storia": "s", "filosofia": "f", "cultura": "c", "mente": "m", "scienza": "x"}
CAMPI = {"id", "c", "k", "t", "b", "l", "m", "q"}
LIMITI = {"k": (2, 30), "t": (10, 60), "b": (200, 400), "l": (30, 130)}


def norm(s):
    return re.sub(r"[^a-z0-9àèéìòù]+", " ", s.lower()).strip()


def main(path):
    errori = []
    try:
        testo = open(path, encoding="utf-8").read()
        dati = json.loads(testo)
    except Exception as e:
        print(f"ERRORE: JSON non valido: {e}")
        return 1
    if not isinstance(dati, list) or not dati:
        print("ERRORE: il file deve essere una lista non vuota")
        return 1
    ids, titoli = set(), {}
    for i, c in enumerate(dati):
        dove = f"scheda {i} ({c.get('id', '?') if isinstance(c, dict) else '?'})"
        if not isinstance(c, dict) or set(c) != CAMPI:
            errori.append(f"{dove}: campi devono essere esattamente {sorted(CAMPI)}")
            continue
        if c["c"] not in CATEGORIE:
            errori.append(f"{dove}: categoria '{c['c']}' non valida")
        elif not re.fullmatch(PREFISSO[c["c"]] + r"\d{2,3}", c["id"]):
            errori.append(f"{dove}: id deve essere '{PREFISSO[c['c']]}' + numero")
        if c["id"] in ids:
            errori.append(f"{dove}: id duplicato")
        ids.add(c["id"])
        if c["m"] not in MOTIVI:
            errori.append(f"{dove}: motivo '{c['m']}' non esiste")
        for f, (lo, hi) in LIMITI.items():
            if not isinstance(c[f], str) or not lo <= len(c[f]) <= hi:
                errori.append(f"{dove}: campo '{f}' lungo {len(str(c[f]))}, ammesso {lo}-{hi}")
        q = c["q"]
        if not (isinstance(q, list) and len(q) == 4 and all(isinstance(x, str) and 1 <= len(x) <= 90 for x in q)):
            errori.append(f"{dove}: 'q' deve essere [domanda, giusta, sbagliata, sbagliata], max 90 caratteri")
        elif len({norm(x) for x in q[1:]}) != 3:
            errori.append(f"{dove}: risposte del quiz non distinte")
        t = norm(c["t"])
        if t in titoli:
            errori.append(f"{dove}: titolo uguale a {titoli[t]}")
        titoli[t] = c["id"]
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
