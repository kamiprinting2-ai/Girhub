#!/bin/bash
# Reel «خبرتنا بين يدينكم»: 3 short real clips (slowed) + 2 photos + end card, 1080x1920. Run from repo root: bash video/works-reel-3/build.sh
set -e
D=video/works-reel-3; P=templates/photos/works; T=$(mktemp -d)
node -e "
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/$D/overlays.html');await p.waitForTimeout(1500);
for(const i of [1,2,3,4,5,6]){await (await p.\$('#t'+i)).screenshot({path:'$D/t'+i+'.png',omitBackground:true});}await b.close();})()"
V='-r 30 -c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 -an'
FILL='split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2+80'
CROP='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920'
clip(){ ffmpeg -y -loglevel error -i $P/$1 -i $D/$2 -filter_complex "[0:v]setpts=$3*PTS,$4[v];[v][1:v]overlay" $V $T/$5.mp4; }
clip v-boxes.mov t1.png 1.6 "$FILL" s1
clip v-thermos.mov t2.png 1.4 "$CROP" s2
clip v-glass.mov t3.png 1.7 "$CROP" s3
i=4; for img in shell-boxes school-sheets; do
ffmpeg -y -loglevel error -loop 1 -t 2.6 -i $P/$img.jpg -i $D/t$i.png -filter_complex "[0:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,zoompan=z='1+0.0015*on':d=78:s=1080x1920:fps=30:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v];[v][1:v]overlay" -t 2.6 $V $T/s$i.mp4; i=$((i+1)); done
ffmpeg -y -loglevel error -loop 1 -t 3 -i $D/t6.png $V -vf "format=yuv420p" $T/s6.mp4
printf "file '%s'\n" $T/s1.mp4 $T/s2.mp4 $T/s3.mp4 $T/s4.mp4 $T/s5.mp4 $T/s6.mp4 > $T/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $T/list.txt -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$D/ريل-خبرتنا.mp4"
rm -rf $T; ffprobe -v error -show_entries format=duration,size -of compact "$D/ريل-خبرتنا.mp4"
