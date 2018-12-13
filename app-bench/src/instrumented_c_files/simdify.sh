# Usage ./simdify DIR VEC_LEVEL
# Scans all files.c in DIR and replaces simdlen(N) with VEC_LEVEL

for file in "$1"/*.c
do
    sed -i "s/simdlen([0-9])/simdlen($2)/g" $file
done
