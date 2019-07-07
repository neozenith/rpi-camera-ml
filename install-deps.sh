#! /usr/bin/bash
__WDIR=$(pwd)

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
# Ignore QT dependency
export ENABLE_HEADLESS=1 
python3 setup.py build
sudo python3 setup.py install

cd $__WDIR 
