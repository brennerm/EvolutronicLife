## Evolutronic Life [![Docker Build Status](https://img.shields.io/docker/build/brennerm/evo_life.svg)](https://hub.docker.com/r/brennerm/evo_life/)

![Alt text](/doc/graphics/screen.png?raw=true)
Text based life simulation with an ongoing fight for survival between plants, carnivores and herbivores.

### Linux Dependencies

- Python 3.X (https://www.python.org/)
- terminal with UTF8 and color support (e.g. Terminator)

### Windows Dependencies

- Cygwin (https://www.cygwin.com/)
- Python 3.X, installable with Cygwin installer
- terminal with UTF8 and color support (e.g. Cygwin Terminal)

### Execution:

$ docker run -ti brennerm/evo_life

or

$ python3 evo\_life


### Parameters

-m <map> / --map=<map>
- selection of map for simulation
- map needs to be one of the .map files in maps folder

-k <num> / --kickstart=<num>
- jump directly to a specific step of the simulation
- previous steps will be calculated without visualization


### Controlling the simulation

- F1: Pause / Continue
- F2: Speed up simulation
- F2: (while paused) stepwise simulation execution
- F3: Slow down simulation
- F4: Exit simulation
- Click on element: Open window with information about element
