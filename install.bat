@echo off
echo "Starting installation. This may take a while..."
winget install --id Git.Git -e --source winget
git clone https://github.com/Jah135/mad-pigeons.git -q
pip install pygame-ce -q
pip install pymunk -q
del ./temp.bat
cd ./mad-pigeons
echo "Installation complete. Run 'python ./madpigeons/main.py' to start Mad Pigeons!"
