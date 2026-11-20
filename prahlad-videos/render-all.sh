#!/bin/bash
# Render, mux and cover each Prahlad episode (resumable). Usage: bash render-all.sh 1 2 3 4 5
P=/home/user/testng/prahlad-videos; L=/root/lemo-opuscar
declare -A DUR=([1]=48.6 [2]=52.3 [3]=48.1 [4]=47.9 [5]=49.5)
declare -A TH=([1]=35.0 [2]=28.0 [3]=33.0 [4]=31.2 [5]=31.0)
for e in "$@"; do
  V=$P/prahlad$e-oil-painting.mp4; [ -f "$V" ] && continue
  N=$(python3 -c "import math;print(math.ceil(${DUR[$e]}*24))"); Q=$((N/4+1)); D=$P/out/frames$e; mkdir -p $D
  cd $L
  for k in 0 1 2 3; do a=$((k*Q)); b=$(( (k+1)*Q < N ? (k+1)*Q : N )); nice node $P/render-frames.mjs $P $D $a $b --q "v=oil&ss=1&ep=$e" > $P/out/log$e.$k 2>&1 & done; wait
  [ $(ls $D | wc -l) -ge $N ] || { echo "ep$e incomplete"; exit 1; }
  ffmpeg -v error -y -framerate 24 -i $D/f_%05d.jpg -i $P/audio/mix${e}_norm.wav -c:v libx264 -crf 24 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart $V.tmp.mp4 && mv $V.tmp.mp4 $V
  for r in 1 2 3; do timeout 400 node core/render/still.mjs $P ${TH[$e]} --size 1080x1920 --q "v=oil&ep=$e&thumb=1" --prefix cover${e}_ >/dev/null 2>&1 && break; done
  cp $P/stills/cover${e}_${TH[$e]}.jpg $P/prahlad$e-cover-1080x1920.jpg 2>/dev/null || cp "$(ls -t $P/stills/cover${e}_* | head -1)" $P/prahlad$e-cover-1080x1920.jpg
  echo "ep$e done"
done
