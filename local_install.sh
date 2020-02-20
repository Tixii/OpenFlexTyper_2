#!/bin/bash

########################################################################
###
### Copyright (c) 2018, Wasserman lab
###
### FILE        test.sh
###
### DESCRIPTION This is the install.sh script for the project
###
### Initial version @ Godfrain Jacques KOUNKOU
###
########################################################################

# set -e

if [[ $(id -u) -ne 0 ]]; then 
   echo "Please run as root"
   exit 1 
fi

# install dependencies
function installDeps() {
   sudo apt-get install -y curl graphviz libdivsufsort-dev libdivsufsort3 libsdsl-dev libsdsl3             \
                           libgtest-dev libboost-all-dev g++-8 gcc-8             						   \
			   			   dialog && apt-get install -y whiptail git zlib1g-dev              			   \
			   			   libbz2-dev cmake wget libx11-dev libdbus-glib-1-2 qt5-qmake libx11-xcb-dev      \
			   			   libglu1-mesa-dev libxrender-dev build-essential qt5-default qtdeclarative5-dev  \
                	       libqt5webview5-dev git-core
}

# build the project
function buildProject() {
   if [ ! -d build ]; then
      mkdir build
   fi

   cd build
   projects=('../')

   for proj in ${projects[@]}; do
      echo $proj
      qmake "$proj"
      make
   done 
}

# install the application
function installApp() {
   mkdir -p /opt/FlexTyper/bin
   cp -rf flextyper /opt/FlexTyper/bin/FlexTyper
   cp -rf flextyper /opt/FlexTyper/bin/flexTyper


   if [ -z $(grep "FlexTyper" "/etc/environment") ]; then 
      sed -i 's|PATH="\(.*\)"|PATH="/opt/FlexTyper/bin:\1"|g' /etc/environment
	  echo 
   fi

   user=$(who | awk -F' ' 'NR==1 {print $1}')
   echo $user
   chmod -R 766 /opt/FlexTyper/*
   chown -R "$user:$user" /opt/FlexTyper/
   chown -R "$user:$user" .
}

installDeps
buildProject
installApp

echo Thank you $user, 'Installation finished ! Please restart the System to use FlexTyper or export PATH=$PATH:/opt/FlexTyper/bin/'
