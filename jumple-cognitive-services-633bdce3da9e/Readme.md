In questa cartella sono presenti 4 librerie *(tts.py, stt.py, face.py, qna.py) * che fanno uso dei Cognitive Services di Microsoft Azure per simulare la user experience raffigurata in questo schema *(MicrosoftServices_TTS_STT_FACE_QNA.py) *.
[![UX](https://bitbucket.org/jumple/cognitive-services/raw/a044409a3ee502edaa6689ec8db38ae3c82216ca/photo/UX-example.png "UX")](https://bitbucket.org/jumple/cognitive-services/raw/a044409a3ee502edaa6689ec8db38ae3c82216ca/photo/UX-example.png "UX")

# Face Recognition (face.py) (API)
Questa libreria contiene diverse funzioni che permettono di creare un "database" per raccogliere, riconoscere ed identificare volti e persone all'interno dello stesso. 
## Funzioni
**create_group_person:** crea un database che verrà di volta in volta popolato con persone e relativi volti. Il parametro personGroupId è una stringa che contiene il nome del gruppo a cui appa rterranno i vari profili (ad es. colleghi, amici, famiglia)

**create_person(personGroupId, name, user_data=None):** crea un profilo/persona (name) da aggiungere al gruppo (personGroupId) specificato.Ritorna un person_id univoco.

**add_face(personGroupId, person_id, target_face=None, user_data=None):**  aggiunge un volto alla persona (person_id) presente nel gruppo (personGroupId)

**train(personGroupId):**  esegue il training dell'algoritmo tenendo conto delle persone e relativi volti presenti in quel gruppo fino a quel momento.

**detect(personGroupId):** riconosce la presenza di uno o più volti all'interno di una foto (senza identificarli). Ritorna i vari IDs dei volti riconosciuti insieme alle cordinate in cui si trovano.

**identify(personGroupId, face_ids, max_candidates_return=1, threshold=None):**  identifica un volto riconosciuto. Ritorna l'id della persona a cui corrisponde il volto riconosciuto.

**get_a_person(personGroupId,personId):**  Ritorna il nome della persona riconosciuta

## Parametri/Variabili da modificare
subscription_face_key = '****'

### Riferimenti:
(API) https://westeurope.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236
(esempio su Pepper) https://translate.google.com/translate?depth=1&hl=it&rurl=translate.google.it&sl=auto&sp=nmt4&tl=it&u=https://qiita.com/CatDust/items/46254e997a111a2e37f5&xid=17259,15700023,15700124,15700186,15700191,15700201,15700237,15700248

# Question and Answer (qna.py) (API)

 (qna_py2.py per la versione di python 2.7) 
 QnA Maker consente di sviluppare un servizio di domande e risposte a partire dal contenuto semistrutturato, ad esempio documenti con domande frequenti, URL e manuali di prodotti. Questo servizio riconosce la domanda dell'utente e dà in output delle risposte in ordine di livello di confidenza.

## Funzioni

**qna.get_answers(content, n_ans):** 
- CONTENT:  stringa che contiene la domanda (per esempio: "A che ora apre questo negozio?")
- N_ANS: rappresenta il numero di risposte da ritornare in ordine di livello di confidenza.
- La funzione ritorna un json contenente le risposte con relativo livello di confidenza.

## Parametri/Variabili da modificare
 host_qna = "xxxx*.azurewebsites.net" 
 endpoint_key_qna = " xxxxx" 
 kb_qna = "xxxxxx"

### Riferimenti:
https://docs.microsoft.com/it-it/azure/cognitive-services/qnamaker/tutorials/create-publish-query-in-portal

#Text To Speech (tts.py) (API) 
Questo servizio converte il testo di input in parlato. Per generare il parlato, l'applicazione invia richieste HTTP POST all'API Sintesi vocale, dove il testo viene sintetizzato in una voce dal suono umano e restituita come file audio.

La classe **TextToSpeech** viene inizializzata ricevendo come parametri la *chiave di sottoscrizione (subscription_key_tts)* e la *stringa* da tradurre in audio. Dopodichè salva l'audio nel file "*/sound/voice.wav"* e lo esegue.

###Riferimento:
https://docs.microsoft.com/it-it/azure/cognitive-services/speech-service/quickstart-python-text-to-speech

# Speech To Text (stt.py) (SDK)
Questo servizio converte un audio in testo. Prima di cominciare a registrare, viene emesso un suono, una volta che il sistema smette di riconoscere la voce emette un altro suono e ritorna una stringa contenente il testo parlato.

### Take a photo (photo.py) 
** take_photo:** semplice funzione che permette di scattare una foto tramite la webcam.

#ESEMPIO: 
##MicrosoftServices_TTS_STT_FACE_QNA.py

###Funzioni
**getRectangle:** funzione necessaria per ottenere i punti top/left e bottom/right del rettangolo.

**say(text,risp=None):** funzione che prende in input un testo e tramite la funzione *TextToSpeech* lo traduce in un comando vocale, se il parametro risp non è nullo allora ritorna anche la risposta dell'utente.

**question(content):** tramite la funzione *get_answers* della libreria QNA, prende in input una domanda e ritorna la risposta con il più alto livello di confidenza (in questo caso è stato utilizzato un database contenente le Q&A di Trenitalia)

### Flusso (main):
[![UX](https://bitbucket.org/jumple/cognitive-services/raw/a044409a3ee502edaa6689ec8db38ae3c82216ca/photo/UX-example.png "UX")](https://bitbucket.org/jumple/cognitive-services/raw/a044409a3ee502edaa6689ec8db38ae3c82216ca/photo/UX-example.png "UX")

- Una volta avviato lo script, viene eseguito il training dell'algoritmo di riconoscimento facciale, viene chiesto all'utente di avvicinarsi alla webcam e di attendere fino a quando almeno un volto non sarà riconosciuto.

- Una volta riconosciuti uno o più volti, si apre un'immagine contenente un rettangolo che riprende il volto che si sta analizzando in quel momento.
 -- Se quel volto non viene identificato (quindi non corrisponde a nessuna persona del gruppo) un messaggio vocale chiederà il nome dell'utente, e già dalla prossima interazione l'utente verrà riconosciuto. 
 -- Se invece il volto viene identificato (quindi una persona è già stata assegnata a quel volto) allora un messaggio vocale saluterà quella persona e le chiederà di porre una domanda (su trenitalia). 
 
- Se il parametro redundancy corrisponde a "yes" allora un messaggio vocale chiederà ulteriore conferma del nome (Sei Pippo?). 
A quel punto se la risposta dell'utente è:
**positiva:** aggiungerà la foto appena scattata al profilo della persona (in modo tale da migliorare l'algoritmo di training) 
**altrimenti: **chiederà di registrare un nuovo nome.

##Parametri/Variabili da modificare
- subscription_key_tts="xxxxxx"
- personGroupId="nome del gruppo"
- format = *"yes"*: permette di cancellare tutti i profili (persona+volti) presenti all'interno di quel personGroupId).
- insertion=*"text"* o *"speech"*: per interagire tramite comandi vocali o riga di comando.
- redundancy=*"yes"*:  una volta identificato un volto, ti chiede se è corretto o meno.

# TEST COMPUTER VISION 
La cartella TEST COMPUTER VISION invece contiene altri esempi di script che usano i Microsoft Services.

##Riferimenti
https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/blob/master/samples/vision/face_samples.py
