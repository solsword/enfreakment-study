#!/bin/sh
mkdir -p cropped
mogrify -crop 960x1080+0+0 -path cropped sfv-ingame*
