#!/usr/bin/env bash

# Creating "~/.bash_aliases" file if it does not exists
if [ ! -f ~/.bash_aliases ]; then
    touch ~/.bash_aliases
fi

# Installing the omegaUp CLI and creating its alias
pip3 install --user . && echo "alias ucli=/home/$USER/.local/bin/ucli" >> ~/.bash_aliases

# If "fish" shell is used, the alias is imported
if command -v fish &> /dev/null
then
    if [ ! -f ~/.config/fish/config.fish ]; then
        touch ~/.config/fish/config.fish
    fi
    echo ". ~/.bash_aliases" >> ~/.config/fish/config.fish
fi

clear && echo "[i] If there are no changes, restart your terminal."
