#!/usr/bin/env bash

# Pregunta por ~./bash_aliases
if [ ! -f ~/.bash_aliases ]; then
    touch ~/.bash_aliases
fi

# Intalacion de la OmegaUp CLI y creacion de un alias
pip3 install --user . && echo "alias ucl=/home/$USER/.local/bin/ucl" >> ~/.bash_aliases

# Importación de los alias a la shell de fish (en caso de ser usuario)
if command -v fish &> /dev/null
then
    if [ ! -f ~/.config/fish/config.fish ]; then
        touch ~/.config/fish/config.fish
    fi
    echo ". ~/.bash_aliases" >> ~/.config/fish/config.fish
fi

clear
echo "[!] Para reflejar los cambios, reinicia tu terminal!"
