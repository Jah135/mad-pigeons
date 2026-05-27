# mad-pigeons
Definitely not an Angry Birds clone.

## Requirements
- Python 3.13+

### Modules
- pymunk - `pip install pymunk`
- pygame (community edition) - `pip install pygame-ce`

## 03 Camp Installation Guide:
TODO: streamline this down into just one command, maybe something with curl?

Use this to download all of the required assets and code:
```bat
@echo off
rmdir "./mad-pigeons" /S /Q
git clone https://github.com/Jah135/mad-pigeons.git
pip install pymunk
pip install pygame-ce
```
then run this to start Mad Pigeons:
```
python ./mad-pigeons/madpigeons/main.py
```
