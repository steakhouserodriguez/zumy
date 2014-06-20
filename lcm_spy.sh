#!/bin/sh

lcm-gen -j types/*.lcm
javac -cp .:lcm.jar fearing/*.java
jar cvf fearing/fearing.jar fearing/*.class
export CLASSPATH=$CLASSPATH:./fearing/fearing.jar
alias java='java -ea -server'
lcm-spy --lcm-url='udpm://239.255.76.67:7667?ttl=1'
