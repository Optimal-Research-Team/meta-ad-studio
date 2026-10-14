#!/bin/sh
# IRV1 (Oct 14, 2026): the one AI video for IV iron. 6.45 s, 9:16 + 4:5.
# kling_raw.mp4 = Higgsfield kling3_0 pro, 9:16, sound off, start_image = gen/r4/IR3_raw.png (job 8dea4870-…; not in git).
# Only 0–2.9 s is used, slowed 1.5x: after ~3 s the recliner's footrest extends on its own.
# The capsule sits on from frame 0 (so a muted autoplay still reads), then crossfades at 3.85 s to the end card.
# Music bed at -38 LUFS (Peter likes it very quiet). brand/audio is licensed and git-ignored.
set -e
cd "$(dirname "$0")"
python3 frames.py
FF=../../../../tools/node_modules/ffmpeg-static/ffmpeg; BED=../../../../brand/audio/bed_built_upon_a_path.wav; OUT=../../../out/r4/iron
mkdir -p $OUT
for R in 9x16 4x5; do
  if [ $R = 9x16 ]; then VF="scale=1084:1920,crop=1080:1920"; else VF="scale=1084:1920,crop=1080:1350:2:330"; fi
  $FF -v error -y -i kling_raw.mp4 -loop 1 -t 4.35 -i ov_$R.png -loop 1 -t 2.6 -i end_$R.png -ss 2 -t 6.6 -i $BED \
   -filter_complex "[0:v]trim=0:2.9,setpts=1.5*(PTS-STARTPTS),minterpolate=fps=30:mi_mode=blend,$VF,setsar=1,format=yuv420p[v0];[1:v]fps=30,format=rgba[ov];[v0][ov]overlay=0:0:format=auto,format=yuv420p[v1];[2:v]fps=30,setsar=1,format=yuv420p[end];[v1][end]xfade=transition=fade:duration=0.5:offset=3.85,format=yuv420p[v];[3:a]aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=0:6.45,asetpts=PTS-STARTPTS,loudnorm=I=-38:TP=-6:LRA=7,afade=t=in:st=0:d=0.6,afade=t=out:st=5.6:d=0.85,aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -t 6.45 -c:v libx264 -profile:v high -preset slow -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -movflags +faststart -map_metadata -1 $OUT/IRV1_$R.mp4
  $FF -v error -y -i $OUT/IRV1_$R.mp4 -frames:v 1 -update 1 $OUT/IRV1_${R}_thumb.jpg
done
echo "IRV1 built in out/r4/iron"
