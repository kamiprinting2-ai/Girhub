#!/bin/bash
# Reel «توزيعات بالاسم»: 2 real clips + 2 photos + end card, 1080x1920. Run from repo root: bash video/works-reel-2/build.sh
set -e
D=video/works-reel-2; P=templates/photos/works; T=$(mktemp -d)
node -e "
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/$D/overlays.html');await p.waitForTimeout(1500);
for(const i of [1,2,3,4,5]){await (await p.\$('#t'+i)).screenshot({path:'$D/t'+i+'.png',omitBackground:true});}await b.close();})()"
V='-r 30 -c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 -an'
# s1: landscape clip on blurred fill
ffmpeg -y -loglevel error -i $P/v-shells.mp4 -i $D/t1.png -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2+120[v];[v][1:v]overlay" $V $T/s1.mp4
ffmpeg -y -loglevel error -i $P/v-teacher.mov -i $D/t2.png -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v];[v][1:v]overlay" $V $T/s2.mp4
i=3; for img in school-pencil school-melon; do
ffmpeg -y -loglevel error -loop 1 -t 2.6 -i $P/$img.jpg -i $D/t$i.png -filter_complex "[0:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,zoompan=z='1+0.0015*on':d=78:s=1080x1920:fps=30:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v];[v][1:v]overlay" -t 2.6 $V $T/s$i.mp4; i=$((i+1)); done
ffmpeg -y -loglevel error -loop 1 -t 3 -i $D/t5.png $V -vf "format=yuv420p" $T/s5.mp4
printf "file '%s'\n" $T/s1.mp4 $T/s2.mp4 $T/s3.mp4 $T/s4.mp4 $T/s5.mp4 > $T/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $T/list.txt -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$D/ريل-توزيعات-بالاسم.mp4"
rm -rf $T; ffprobe -v error -show_entries format=duration,size -of compact "$D/ريل-توزيعات-بالاسم.mp4"
