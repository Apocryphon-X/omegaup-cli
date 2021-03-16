#!/usr/bin/env bash

# Pregunta por ~./bash_aliases
if [ ! -f ~/.bash_aliases ]; then
    touch ~/.bash_aliases
fi

# Instalacion de OmegaUp CLI, y creacion de un alias.
pip3 install --user . && echo "alias ucl=/home/$USER/.local/bin/ucl" >> ~/.bash_aliases

# En caso de ser usuario de "fish", se importa el alias creado.
if command -v fish &> /dev/null
then
    if [ ! -f ~/.config/fish/config.fish ]; then
        touch ~/.config/fish/config.fish
    fi
    echo ". ~/.bash_aliases" >> ~/.config/fish/config.fish
fi

clear && echo "[!] Si no se reflejan los cambios, reinicia tu terminal!"
