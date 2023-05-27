#!/usr/bin/env bash

# This script runs after the container is created.

PDM_VERSION="2.5"


pip3 install --user "pdm~=$PDM_VERSION"
pdm sync
pre-commit install

# Activate pdm completion

# post create script does not work with zsh variables
# possible a bug: https://github.com/microsoft/vscode-remote-release/issues/6841
ZSH_CUSTOM="/home/vscode/.oh-my-zsh/custom"

mkdir $ZSH_CUSTOM/plugins/pdm
pdm completion zsh > $ZSH_CUSTOM/plugins/pdm/_pdm
sed -i 's/plugins=(.*/plugins=(git pdm)/g' ~/.zshrc
