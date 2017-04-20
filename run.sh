#!/usr/bin/env bash

d=`dirname $0`;
cd "$d";
source ENV/bin/activate;
python main.py;
