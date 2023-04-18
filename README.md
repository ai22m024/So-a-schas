# So-a-schas
Ein empirischer Vergleich zwischen Extractive und Abstractive Summarizer. Das besondere ist, dass die Reviews zuvor auf negatives Sentiment gefiltert wurden. 

## Wiener Schmäh trifft NLP
## **Installation**
    pip install -r requirements.txt
    python -m textblob.download_corpora

## **Usage**

! Einige Modelle können recht groß sein. Beim ersten Start könnte es länger dauern, bis die Checkpoints heruntergeladen wurden. !

- ## CLI Tool
        python summarize_cli.py

- ## Web Interface
    In 2 verschiedenen Konsolen starten:

        python src\client\client.py.py
        python src\api\api.py
   
    Im Browser: http://127.0.0.1:5000

- ## Notebook
        generate_reviews.ipynb


# So a schas. Die Schmankerl.

**Die besten negativsten Kommentare des NLP-Projekts von Michael Schwingshackl und Marvin Elias.**

## Abstractive: 

- Gute Schmankerl:
	- Billa Praterstern:<br>
		Man darf nur eine begrenzte Anzahl an Personen reinlassen, weil man sich sonst nicht bewegen kann.
	- Ferhat Döner:<br>
		Der kalte Döner ist auf den Tresen geschmissen.
	- Obi Triester Straße:<br>
		Die Auswahl ist ok, das Fachpersonal scheint sich vor den Kunden zu verstecken.
	- Praterdome:<br>
		In meiner eigenen Stadt kann ich nicht einmal in einem Club reingehen.
	- TU Wien:<br>
		Nie nie wieder.Organisatorisch das reinste Chaos.

- Schlechte Schmankerl:
	- Ferhat Döner:<br>
		Der Verkäufer hat seinen Verkäufer kaputt verkauft und er hat es geschafft
	- Hofburg:<br>
		Die Ärgernisse in der deutschen Popkultur sind eher ernst.
	- Praterdome:<br>
		Die Innenstadt ist wegen der hohen Temperaturen ziemlich kalt

## Extractive:
- Gute Schmankerl:
	- Billa Praterstern:<br>
		Er fetzte meine Sachen regelrecht übers Band. Aber Hauptsache zu seinem Landsmann, der vor mir dran war, war er überaus freundlich.
	- Ferhat Döner:<br>
		Eine Stunde Wartezeit für einen geschmacklich unterdurchschnittlichen Döner. Zudem alles leider nicht sehr hygienisch und sauber vor Ort.
	- Hofburg:<br>
		Momentan Sitz der Österreichischen Volksverräter
	- Obi Triester Straße:<br>
		Muss an einem weniger frequentierten Werktag bequemer sein
	- Praterdome:<br>
		Eher typischer touristen cash grab.
	- TU Wien:<br>
		Totaler Schwachsinn, geh lieber aufs Technikum!