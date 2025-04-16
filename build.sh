#!/bin/bash

# Make bin folder
mkdir -p bin

# Download Chrome (headless) binary
wget -O chrome-linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/123.0.6312.86/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
mv chrome-linux64/chrome bin/headless-chrome
rm -rf chrome-linux64.zip chrome-linux64

# Download matching chromedriver
wget -O chromedriver-linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/123.0.6312.86/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver bin/chromedriver
rm -rf chromedriver-linux64.zip chromedriver-linux64

# Make them executable
chmod +x bin/headless-chrome bin/chromedriver
