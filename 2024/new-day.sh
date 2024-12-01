#!/bin/zsh

mkdir day-$1
cd day-$1
FILENAME="day_$1.py"
cat << EOF > $FILENAME
#!/usr/bin/env python

with open('test.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

EOF
chmod +x $FILENAME
touch test.txt
touch input.txt