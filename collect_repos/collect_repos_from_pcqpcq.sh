#!usr/bin/env sh

git clone https://github.com/pcqpcq/open-source-android-apps/
grep -irho "https://github.com/\(\w\|-\)\+/\(\w\|-\)\+" open-source-android-apps/categories | sort | uniq | cut -d / -f4 -f5 | sed 's/\//,/g'
rm -rf open-source-android-apps
