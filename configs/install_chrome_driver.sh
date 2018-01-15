## Chromedriver
OLD=$PWD
cd /tmp
wget --no-check-certificate https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo chmod +x chromedriver
sudo mv chromedriver /usr/bin/
rm chromedriver_linux64.zip
cd $OLD
