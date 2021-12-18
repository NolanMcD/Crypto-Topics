#
# makefile for proj2
# author: bjr
# date: 30 aug 2021
#

SOLVED_KEY= themystery

ST= standard-text.txt
PT= plaintext.txt
CT= ciphertext.txt

REF_FILE= proj2-ref
#VERBOSE= -v
#MF= -f Makefile
PY= python3

RED= \033[0;31m
GREEN= \033[0;32m
NC= \033[0m

all:
	make ${MF} test-1
	make ${MF} test-2	
	make ${MF} test-3	
	make clean

rot13:
	cp ${ST} ${PT}
	make ${MF} KEY="m" encrypt
	rm ${PT}

keylen2:
	cp ${ST} ${PT}
	make ${MF} KEY="my" encrypt

keylen3:
	cp ${ST} ${PT}
	make ${MF} KEY="mys" encrypt

encrypt:
	cat ${PT} | ${PY} vigenere.py ${KEY} > ${CT}

test-1: 
	cat ${ST} | ${PY} letter-utils.py -s 0 ${ST} > run.out
	diff -w run.out ${REF_FILE}1.ref
	@echo "*** ${GREEN}PASSED the test ${NC}***"

test-2: rot13
	cat ${CT} | ${PY} letter-utils.py -s 0 ${ST} > run.out
	diff -w run.out ${REF_FILE}2.ref
	@echo "*** ${GREEN}PASSED the test ${NC}***"

test-3: keylen2
	cat ${CT} | ${PY} letter-utils.py ${ST} > run.out
	awk '{print $$4}' run.out > numbers-for-excel.txt
	diff -w run.out ${REF_FILE}3.ref
	@echo "*** ${GREEN}PASSED the test ${NC}***"

challenge: 
	cat challenge.txt | ${PY} vigenere.py ${SOLVED_KEY} > secret-message.txt

clean:
	-rm run.out ${PT} ${CT} numbers-for-excel.txt

