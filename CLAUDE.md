# Agorà — istruzioni per gli aggiornamenti

App di micro-apprendimento stile TikTok (PWA su GitHub Pages: https://carlinodiego146-bit.github.io/AGOR-/).
L'app legge `cards.json` all'avvio; ogni scheda con un `id` nuovo compare come novità nel feed.

## Regole fisse
- Modifica solo `cards.json` (ed eventualmente `strumenti/`). Non toccare `index.html`, `sw.js`, `manifest.webmanifest` o le icone se non è stato chiesto esplicitamente.
- Non rinominare il repository e non cambiare il ramo `main`: l'app installata dipende dall'indirizzo `/AGOR-/`.
- Prima di ogni push: `python3 strumenti/verifica.py` deve stampare `OK`. Se fallisce, correggi; se non riesci, non pubblicare.
- Mai cancellare o modificare schede esistenti (si perderebbero progressi e ripassi dell'utente), salvo errore fattuale evidente.

## Formato di una scheda (una per riga in `cards.json`)
`{"id":"s45","c":"storia","k":"1492","t":"Titolo","b":"Testo","l":"Lezione","m":"globe","q":["Domanda?","Risposta giusta","Sbagliata","Sbagliata"]}`
- `id`: prefisso di categoria + numero successivo al più alto esistente (storia `s`, filosofia `f`, cultura `c`, mente `m`, scienza `x`).
- `c`: storia | filosofia | cultura | mente | scienza.
- `k`: sopratitolo breve (data, epoca, autore o ambito), 2–30 caratteri.
- `t`: titolo-gancio, 10–60 caratteri, che incuriosisce ("Napoleone non era basso").
- `b`: corpo, 200–400 caratteri, fatti concreti e verificabili, niente frasi vuote.
- `l`: la lezione in una frase, 30–130 caratteri.
- `m`: un motivo grafico tra quelli ammessi in `strumenti/verifica.py` (MOTIVI), coerente col tema.
- `q`: quiz di ripasso; la risposta giusta è SEMPRE il secondo elemento; risposte sbagliate plausibili.

## Stile
- Italiano corretto e scorrevole, tono da divulgatore brillante. Virgolette «basse».
- Solo fatti solidi e consolidati. Niente aneddoti dubbi o leggende spacciate per fatti: se un mito è famoso, la scheda può smontarlo.
- Niente doppioni: controlla titoli e argomenti già presenti prima di scrivere (stesso personaggio + stesso fatto = doppione).
- Varietà: epoche, luoghi e autori diversi, non solo Europa.
