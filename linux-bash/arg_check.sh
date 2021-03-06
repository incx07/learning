#!/usr/bin/env bash

# BASH script which takes one arg as input. 
# In script, check the type of the arg and perform an action:
# 1) if it is ELF executable, print ".rodata" section of the file
# 2) if arg name ends with ".txt", append the current time to the end of this file
# 3) if arg is a number (integer number) and it is a PID of running process, 
#    print the 'cmdline' used to run this process, 
#    if not a PID - add '1000' and print this sum to console.


if [[ $# -ne 1 ]]; then
    echo "$# parameters were passed. 1 is required."
elif [[ -f $1 ]]; then
    file -b "$1" | grep -q '^ELF.*executable'
    if [[ $? -eq 0 ]]; then
        readelf -p .rodata $1
    elif [[ $1 == *".txt" ]]; then
        'date' >> "$1"
    else
    echo "Invalid parameter."
    fi
elif [[ $1 =~ ^[0-9]+$ ]]; then
    ps -A -o pid | grep -q "^ *$1$"
    if [[ $? -eq 0 ]]; then
        cat /proc/"$1"/cmdline
        echo -e
    else 
    SUM=$(( $1+1000 ))
    echo $SUM
    fi
else
echo "Invalid parameter."
fi
