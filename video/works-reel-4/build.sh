#!/bin/bash
# Reel «طلب دانة»: cutting clip + 3 photos + packing clip + end card, 1080x1920. Run from repo root: bash video/works-reel-4/build.sh
set -e
D=video/works-reel-4; P=templates/photos/works; T=$(mktemp -d)
node -e "
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/$D/overlays.html');await p.waitForTimeout(1500);
for(const i of [1,2,3,4,5,6]){await (await p.\$('#t'+i)).screenshot({path:'$D/t'+i+'.png',omitBackground:true});}await b.close();})()"
V='-r 30 -c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 -an'
CROP='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920'
still(){ ffmpeg -y -loglevel error -loop 1 -t 2.4 -i $P/$1.jpg -i $D/$2 -filter_complex "[0:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,zoompan=z='1+0.0015*on':d=72:s=1080x1920:fps=30:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v];[v][1:v]overlay" -t 2.4 $V $T/$3.mp4; }
still dana-shell t1.png s1
ffmpeg -y -loglevel error -i $P/v-dana-cutting.mov -i $D/t2.png -filter_complex "[0:v]setpts=1.3*PTS,$CROP[v];[v][1:v]overlay" $V $T/s2.mp4
still dana-ribbons t3.png s3
still dana-note t4.png s4
ffmpeg -y -loglevel error -i $P/v-dana-packing.mov -i $D/t5.png -filter_complex "[0:v]$CROP[v];[v][1:v]overlay" $V $T/s5.mp4
ffmpeg -y -loglevel error -loop 1 -t 3 -i $D/t6.png $V -vf "format=yuv420p" $T/s6.mp4
printf "file '%s'\n" $T/s1.mp4 $T/s2.mp4 $T/s3.mp4 $T/s4.mp4 $T/s5.mp4 $T/s6.mp4 > $T/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $T/list.txt -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$D/ريل-طلب-دانة.mp4"
rm -rf $T; ffprobe -v error -show_entries format=duration,size -of compact "$D/ريل-طلب-دانة.mp4"
