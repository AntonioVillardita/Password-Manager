
![](preview%201.png)
![](preview%202.png)
![](preview%203.png)
![](preview%204.png)

# Gestore Password

## Descrizione

Si tratta di un Gestore Password fatto in Python con la moderna interfaccia grafica "**CustomTkinter**".  
Per chi non conosce, prima in maniera catacea si tenevano raggruppati tutti i dati quali nome utente, mail e password, dove c'è il rischio di perderli, o che vada in mano a qualcuno, o che si rovini o strappi il foglio, mentre questa è una soluzione digitale che permette di abbandonare la carta, tenendo raggruppato tutto il necessario.  
Quasi interamente fatto con IA, ma sempre con la mia supervisione al codice.

## Funzionamento/Esempio di Utilizzo

L'app parte inizialmente con una schermata "Login" di creazione ***Vault***, dove chiede di inserire una ***Master Password***. Questa è la **MADRE** di tutte le vostre password, perchè prima si deve accedere al vostro "**Vault**" attraverso la **Master Password** e poi potrete accedere a tutti i vostri dati (per aumentare il livello di sicurezza) quindi non dimenticate **MAI** la **MASTER PASSWORD**.  

Dopo aver creato un **Vault**, sarete nella Home con un display che mostra tutti i dati salvati e di sotto sono presenti 3 barre per inserire i dati necessari per essere salvati.  

Nella barra "Username" potrete mettere o solo il **Nome Utente** o solo l'**Email** o entrambi.  

Il tasto "Aggiungi/Aggiorna" serve sia per salvare nuovi dati, mentre se volete modificare quelli di una piattaforma che avete già salvato, serve inserire nelle 3 barre i nuovi 3 dati, **ASSICURATEVI** che il **NOME** della piattaforma sia **CORRETTO** e vedrete le modifcihe apportate correttamente.  

Nel momento in cui vorrete recuperare una Password salvata, dovrete soltanto inserire il **NOME** della Piattaforma nella barra **"Sito"** e poi premere il tasto "**Copia Password**" e verrà automaticamente copiata negli appunti, pronta per essere incollata.

Per eliminare una voce o i dati di una piattaforma, serve soltanto inserire il **NOME** della Piattaforma nella barra **"Sito"** e poi premere il tasto "**Elimina**" per cancellarla **DEFINITIVAMENTE**.

Il tasto "**Esci**" serve per tornare alla schermata di Login.

## Dettagli Struttura

Dopo la creazione del "***Vault***" il software crea un file "**vault.json**" che fa da "database" per permettere di salvare/caricare i dati all'occorrenza.

Per ragioni di ***sicurezza***, ho applicato i seguenti accorgimenti:

- La creazione di una "**Master Password**" come accesso al **Vault**.
- La password digitata nella barra "**Password**" viene mostrata attraverso i "*" per ogni carattere inserito.
- Dopo la copia della Password tramite il click al tasto "**Copia Password**", la password viene copiata direttamente negli appunti pronta per essere incollata ma **SOLO PER 15 SECONDI**.
- La scrittura del file "**vault.json**" e di **TUTTI** i dati al suo interno, viene applicata attraverso un sistema di ***CRITTOGRAFIA*** chiamato "**Fernet**" tramite la Libreria "**cryptography**".

## Installazione

**È richiesta la versione minima v3.7 di Python.**  
[Aggiorna](https://www.python.org/downloads/)

**Installa il Framework grafico moderno da terminale:**  
```
pip install customtkinter
```

**Installa la Libreria per la Crittografia**
```
pip install cryptography
```
