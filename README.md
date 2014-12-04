--- Evolutronic Life ---

Textbasiertes Simulationsprogramm. Pflanzen, Pflanzenfresser und
Fleischfresser stehen im Wettstreit um die Vorherrschaft in der Natur.


-- Linux --

Abhängigkeiten:
-> Python 3.X (https://www.python.org/)
-> UTF8-fähiges und farbfähiges Terminal (z.B. Terminator)

Programmstart:
-> Navigation in Programmordner
-> $python3 evo\_life


-- Windows --

Abhängigkeiten:
-> Cygwin (https://www.cygwin.com/)
-> UTF8-fähiges und farbfähiges Terminal (Cygwin Terminal)
-> Python 3.X, installierbar über Cygwin installer

Programmstart
-> Navigation in Programmordner
-> $python3 evo\_life


-- Parameter für Programmstart --

-m<map> / --map=<map>
-> Auswahl der Karte für die Simulation
-> muss eine der im Ordner 'maps' enthaltenen .map Dateien sein

-k<num> / --kickstart=<num>
-> Anzahl von Durchläufen ohne visuelle Darstellung
-> Effekt ist Sprung auf die entsprechende Generation


-- Steuerung der Simulation --

F1: Pause / Fortsetzen der Simulation
F2: Beschleunigung der Simulation
F2: (im Pausemodus) Simulation schrittweise ausführen
F3: Verlangsamung der Simulation
F4: Beendigung des Programms
Mausklick auf Element: Aufruf eines Anzeigefensters mit Elementinformationen
