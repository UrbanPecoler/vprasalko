# Vprašalko
Spletna stran za vprašanja in dogovore. Projekt pri predmetu Računalništvo, na Fakulteti za matematiko in fiziko. 

# Funkcionalnost
Spletni vmesnik omogoča delo z več uporabniki hkrati, ki se lahko registrirajo ali pa uporabljajo stran anonimno.<br>
Če uporabnik ni prijavljen, lahko stran uporablja za:
* Ogled vseh vprašanj
* Filtriranje vprašanj po datumu, ogledih ali številu odgovorov
* Ogled profila drugih uporabnikov
* Ogled posameznega vprašanja z vsemi odgovori
<!-- -->
Če pa se uporabnik registrira ali prijavi s svojim uporabniškim imenom in geslom, pa ima poleg vsega že naštetega možnost tudi:
* Pisanja vprašanj in odgovorov
* Urejanja in brisanja svojih vprašanj ali odgovorov
* Urejanja profila (npr. dodati opis ali spremeniti uporabniško ime)
<!-- -->
Da je stran bolj pregledna pri velikem številu vprašanj ali odgovorov, pa uporablja tudi oštevilčene strani, kjer je na eni strani največ 5 vnosov.

# Instalacija
Za program potrebujete [Python 3.x](https://www.python.org/downloads/)<br>
<br>
Instalacija na MacOS:<br>

    # Kloniraj repozitorij
    git clone https://github.com/UrbanPecoler/vprasalko

    # Premakni se v to mapo
    cd vprasalko

    # Nalozi vse potrebne pakete
    pip3 install -r read requirements.txt

    # Zazeni program
    python3 run.py
<br>
Instalacija na Windows sistemu:<br>

    # Kloniraj repozitorij
    git clone https://github.com/UrbanPecoler/vprasalko

    # Premakni se v to mapo
    cd vprasalko

    # Nalozi vse potrebne pakete
    pip install -r read requirements.txt

    # Zazeni program
    python run.py

# Viri
Pri oblikovanju strani sem si zgledoval po strani [StackOverflow](https://stackoverflow.com/)<br>
Za pomoč pri pisanju kode pa sem uporabljal:
* [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
* [StackOverflow](https://stackoverflow.com/)
* [Corey Schafer: Python Flask tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
* [Bootstrap documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
* [W3Schools](https://www.w3schools.com/)