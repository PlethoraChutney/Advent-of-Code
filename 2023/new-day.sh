#!/bin/zsh

mkdir day-$1
echo "#!/usr/bin/env python" > day-$1/day_$1.py
chmod +x day-$1/day_$1.py