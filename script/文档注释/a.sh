#!/bin/bash#!/bin/bash
nohup java -jar cmt-1.0-SNAPSHOT.jar /home/luowangda/LDpacong/datacollect/mnireplus/ld1process  > ld1.log 2>&1 &
nohup java -jar cmt-1.0-SNAPSHOT.jar /home/luowangda/LDpacong/datacollect/mnireplus/ld2process  > ld2.log 2>&1 &
nohup java -jar cmt-1.0-SNAPSHOT.jar /home/luowangda/LDpacong/datacollect/mnireplus/ld3process  > ld3.log 2>&1 &
