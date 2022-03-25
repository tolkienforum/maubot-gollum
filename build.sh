#!/bin/bash

rm maubot-gollum.mbp
zip -9r maubot-gollum.mbp . -x "virtualenv/*" ".git/*" ".idea/*" "build.sh" ".gitignore"
