# Basis Registratie Ondergrond (BRO) Kwaliteitssservices (voorheen BRO data analyse)
De app is een dashboard/webapplicatie om inzicht te verkrijgen in de data uit de BRO. Dit is een handleiding om de code lokaal werkend te krijgen op Windows en Linux

## Benodigdheden
- Python 3.8
- Docker of MongoDb (min 4.2.12) + eventueel mongoDb compass 
- Node.js

## Python virtual environment aanmaken
- Maak een virtual environment aan voor het project met `python3 -m venv PAD`
- Gebruik de virtual environment, dit kan op twee manieren:
   - Doe in Visual Studio Code: ctrl+ shift + P, 'Select Interpreter' en kies de venv waarbij het pad overeenkomt met deze repository.
   - Indien dit niet werkt, activeer de virtual environment via een commando:
      - Windows: `.\PAD\scripts\activate.bat`.
      - Linux: `source PAD/bin/activate`
- Verifieer dat je de goede interpreter gebruikt met `python -c "import sys; print(sys.prefix)"`, deze hoort de map ./PAD aan te geven.

## Environment file configureren
- Kopieër `.env.example` naar `.env` en pas de variabele `absolutePathToRepository` aan in `.env`.

## Path en environment variabelen zetten
- Zet het PYTHONPATH voor Python in de virtual environment goed: 
   - in Linux met `export PYTHONPATH=$PYTHONPATH:/<repository_parent_path>/BROMonitor/app`
   - in Windows met `set PYTHONPATH=<repository_parent_path>/BROMonitor/app`

## Dependencies installeren
-  Installeer de benodigde python packages met `pip install -r ./app/backend/requirements.txt -r ./app/etl/requirements.txt -r ./app/bromonitorgenerator/requirements.txt`
-  Matplotlib kan lokaal in een windows omgeving niet gebouwd worden, installeer het los met 
   -  `python -m pip install -U pip`
   -  `python -m pip install -U matplotlib`
-  Installeer de benodigde npm packages met `npm install --force` in `/app/frontend` folder. TODO: geeft momenteel errors, werkt alleen met `npm install --force`.

## Databases vullen
### Database starten
- Indien je Docker gebruikt: ga naar /db en start de database middels `docker compose up -d`. De database is nu beschikbaar op `localhost:27017`. Mongo express, een web-based viewer, is beschikbaar op `localhost:8081`.
- Indien je geen Docker gebruikt: ga naar de `.env` file en pas het pad naar de database aan zoals gewenst

### Data importeren
- Download de data vanuit Pdok. Run vanuit `app/etl`: `python extract/main.py`
- Importeer de data in MongoDb. Run vanuit `app/etl`: `python load/mongodb/main.py`
- Start de backend. Run vanuit `app/backend`: `uvicorn main:app`
- Creëer statische assets voor de front-end. Run vanuit `app/bromonitorgenerator`: `python main.py`.

## Runnen
-  Start de backend met `uvicorn main:app` in de `/app/backend` folder
-  Start de frontend met `npm run start` in de `/app/frontend` folder
-  De site is nu te bezoeken op `http://localhost:8080`
