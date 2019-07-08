#! /usr/bin/bash
__WDIR=$(pwd)

sudo apt-get install libgtk2.0-dev pkg-config qt4-default -y

PIP="sudo python3 -m pip"
DEPS=$HOME/.deps 

mkdir -pv $DEPS 
if [ ! -d $DEPS/opencv-python/.git ]; then
  git clone https://github.com/skvark/opencv-python $DEPS/opencv-python
fi

cd $DEPS/opencv-python
git checkout master 
git reset --hard
git clean -df
git pull

python3 setup.py build
sudo python3 setup.py install

$PIP install imutils

cd $__WDIR 
