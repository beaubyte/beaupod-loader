#!/bin/bash

PROJECT_DIR=${PWD} # gets current directory

# makes the folders for ffmpeg stuff
mkdir -p "$PROJECT_DIR/ffmpeg_sources"
mkdir -p "$PROJECT_DIR/ffmpeg_build"
mkdir -p "$PROJECT_DIR/bin"

# cds into ffmpeg_sources and wgets the latest ffmpeg version and unzips it
cd "$PROJECT_DIR/ffmpeg_sources" && \
wget -O ffmpeg-8.0.tar.bz2 https://ffmpeg.org/releases/ffmpeg-8.0.tar.bz2 && \
tar xjvf ffmpeg-8.0.tar.bz2 && \
cd ffmpeg-8.0 && \

# creates PATH variable 
PATH="$PROJECT_DIR/bin:$PATH" PKG_CONFIG_PATH="$PROJECT_DIR/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$PROJECT_DIR/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$PROJECT_DIR/ffmpeg_build/include" \
  --extra-ldflags="-L$PROJECT_DIR/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --ld="g++" \
  --bindir="$PROJECT_DIR/bin" \
  --enable-gpl \
  --enable-libfdk-aac \
  --enable-nonfree && \

# compiles the ffmpeg
PATH="$PROJECT_DIR/bin:$PATH" make && \
make install && \
hash -r

echo "Script Finished: Compiled FFmpeg should be installed to: $PROJECT_DIR/bin/ffmpeg"
