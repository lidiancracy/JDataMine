#!/bin/sh

# nohup python len.py "/home/luowangda/LDpacong/datacollect/mnireplus/ld1process" "ld1" >> "ld1.log" 2>&1 &
nohup python len.py "/home/luowangda/LDpacong/datacollect/mnireplus/ld2process" "ld2" >> "ld2.log" 2>&1 &
nohup python len.py "/home/luowangda/LDpacong/datacollect/mnireplus/ld3process" "ld3" >> "ld3.log" 2>&1 &
