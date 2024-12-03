#!/bin/zsh

mkdir day-$1
cd day-$1
FILENAME="day-$1.py"
cat << EOF > $FILENAME
#!/usr/bin/env python
import sys

with open(sys.argv[1], "r") as f:
    lines = [x.rstrip() for x in f]

EOF
chmod +x $FILENAME
touch test.txt
touch input.txt