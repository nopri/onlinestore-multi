#!/bin/sh

#basic variables
BASE=`pwd`
BASEDOMAIN="$BASE/domain"
BASEAPP="$BASE/app"
DEFCONFIG="$BASEAPP/config.ini.dist"
DEFAPP="../../app/app.py"

#check needed file
if [ ! -e "$BASEAPP" ] || [ ! -e $DEFCONFIG ] || [ ! -e $BASEDOMAIN ]  
then
    echo "ERROR: Please run inside application directory"
    exit 3
fi

#check argument
if [ -z "$1" ]
then
	echo "usage: $0 <domain>"
	exit 1
fi


#newdomain variables
NEWDOMAIN="$BASEDOMAIN/$1"
NEWCONFIG="$NEWDOMAIN/config.ini"
NEWAPP="$NEWDOMAIN/app.py"

#is domain exists?
if [ -e "$NEWDOMAIN" ]
then
    echo "ERROR: $NEWDOMAIN already exists."
    exit 2
fi



##action
#mkdir
echo "DOMAIN"
if [ ! -e $NEWDOMAIN ]
then
    mkdir -vp "$NEWDOMAIN"
fi
echo

#config
echo "CONFIG"
if [ ! -e $NEWCONFIG ]
then
    cp -av $DEFCONFIG  $NEWCONFIG
fi
echo

#app.py
echo "APPLICATION"
if [ ! -e $NEWAPP ]
then
    ln -sfv $DEFAPP  $NEWAPP
fi
echo
##

#all done
echo "DONE"
echo "Please edit $NEWCONFIG"
#
