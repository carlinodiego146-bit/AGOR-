# Agorà — istruzioni per gli aggiornamenti

App di micro-apprendimento stile TikTok (PWA su GitHub Pages: https://carlinodiego146-bit.github.io/AGOR-/).
L'app legge `cards.json` all'avvio; ogni scheda con un `id` nuovo compare come novità nel feed.
**Le schede sono in inglese**: l'utente è italiano e usa l'app anche per migliorare l'inglese. Solo le traduzioni del vocabolario sono in italiano.

## Regole fisse
- Modifica solo `cards.json` (ed eventualmente `strumenti/`). Non toccare `index.html`, `sw.js`, `manifest.webmanifest`, le icone o la cartella `preview/` se non è stato chiesto esplicitamente.
- Non rinominare il repository e non cambiare il ramo `main`: l'app installata dipende dall'indirizzo `/AGOR-/`.
- Prima di ogni push: `python3 strumenti/verifica.py` deve stampare `OK`. Se fallisce, correggi; se non riesci, non pubblicare.
- Mai cancellare o modificare schede esistenti (si perderebbero progressi e ripassi dell'utente), salvo errore fattuale evidente.

## Formato di una scheda (una per riga in `cards.json`)
`{"id":"s45","c":"storia","k":"Rome, 1527","t":"Hook title","p":["Page one…","Page two…"],"l":"The takeaway.","m":"crown","v":["sword","map"],"w":[["word","parola"],["phrasal verb","traduzione"],["word","parola"]],"q":["Question?","Right answer","Wrong answer","Wrong answer"]}`
- `id`: prefisso di categoria + numero successivo al più alto esistente (storia `s`, filosofia `f`, cultura `c`, mente `m`, scienza `x`).
- `c`: storia | filosofia | cultura | mente | scienza (chiavi interne, restano in italiano).
- `k`: sopratitolo breve in inglese (place and date, era, author or field), 2–32 caratteri.
- `t`: titolo-gancio in inglese, 10–70 caratteri, che incuriosisce ("Napoleon wasn't short").
- `p`: le pagine che si scorrono in orizzontale. Di norma 2, al massimo 3; ciascuna 1–2 frasi, 80–230 caratteri (la verifica accetta 60–260), totale massimo 600. Ogni pagina deve reggersi da sola.
- `l`: la lezione in una frase, 30–140 caratteri.
- `m`: motivo grafico della copertina; `v`: un motivo per ogni pagina di `p`, scelto in base a ciò che dice quella pagina. Solo motivi dell'elenco MOTIVI in `strumenti/verifica.py`.
- `w`: 3 parole o espressioni utili a un italiano di livello B1–B2, scritte ESATTAMENTE come compaiono nel testo delle pagine, con la traduzione italiana nel senso in cui sono usate lì (es. verbo coniugato).
- `q`: quiz di ripasso in inglese; la risposta giusta è SEMPRE il secondo elemento; risposte sbagliate plausibili.
- Numeri: se una pagina contiene un numero chiave (anno, misura, percentuale), scrivilo in cifre ("1,600 metres", "54%", "2560 BC"): l'app lo mostra grande con un'animazione.

## Stile
- Inglese chiaro (B1–B2), frasi brevi, ortografia britannica, tono da divulgatore brillante.
- Per le citazioni usa le virgolette curve “ ”: mai virgolette dritte dentro i testi.
- Solo fatti solidi e consolidati. Niente aneddoti dubbi o leggende spacciate per fatti: se un mito è famoso, la scheda può smontarlo.
- Niente doppioni: controlla titoli e argomenti già presenti prima di scrivere (stesso personaggio + stesso fatto = doppione).
- Varietà: epoche, luoghi e autori diversi, non solo Europa.
