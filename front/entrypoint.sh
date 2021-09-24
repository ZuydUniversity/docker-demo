#!/bin/bash
## LET OP!: Regel 1 is niet een gewone comment. Zonder deze regel
## bestaat de kans dat het entrypoint script niet werkt. Deze regel
## is een zogenaamde Shebang regel, welke aangeeft met welk programma
## het script gedraait moet worden (in dit geval met Bash, de standaard
## shell voor Unix achtige operating systems).
gunicorn -b 0.0.0.0:5000 app:app