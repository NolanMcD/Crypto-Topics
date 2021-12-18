#
# makefile for csc507/609 semester 221
# author: bjr
# last-update: 
#		22 oct 2019 -bjr:
#		10 oct 2021 -bjr;
#


LIB= PYTHONPATH="../modules:../../class/modules"
PY3= python3
#VERBOSE= -v
VERBOSE=

F= padding_attack.py

PWD= "the key phrase" 
HELLO_WORLD= "hello world"
GETTYSBURG= "Now we are engaged in a great civil war,testing whether that nation, or any nation so conceived and so dedicated,can long endure."

RED= \033[0;31m
GREEN= \033[0;32m
NC= \033[0m


all:
	@echo "\n${GREEN}Makefile for project 4${NC}"
	@echo "\t1.remember to create the ../modules directory"
	@echo "\t2. run ${RED}make sanity-check${NC}"	
	@echo "\t3. modify padding_attack.py\n"	
	make clean



attack-hw: hello-world.enc
	cat hello-world.enc | ${LIB} ${PY3} ${F} ${VERBOSE} --mode attack ${PWD}

hello-world.enc:
	echo ${HELLO_WORLD} | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD} > $@

attack-hc: hungry-caterpiller.enc
	cat hungry-caterpiller.enc | ${LIB} ${PY3} ${F} ${VERBOSE} --mode attack ${PWD}

hungry-caterpiller.enc:
	echo "The Very Hungry Caterpiller!" | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD} > $@



attack-tests:
	echo "fifteen bytes." | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F} ${VERBOSE} --mode attack ${PWD}
	-rm zero.in
	touch zero.in
	cat zero.in | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F} ${VERBOSE} --mode attack ${PWD}



PWD2= "you do not know this password"

challenge-one:
	cat challenge-one.enc | ${LIB} ${PY3} ${F} ${VERBOSE} --mode attack ${PWD2}

challenge-two:
	cat challenge-two.enc | ${LIB} ${PY3} ${F} ${VERBOSE} --mode attack ${PWD2}

create-challenge:
	cat challenge-one.txt | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD2} > challenge-one.enc
	cat challenge-two.txt | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD2} > challenge-two.enc



sanity-check:
	@echo ""
	@echo "*** ${RED}checking for modules ${NC}***"
	ls ../modules/bohzu_aes.py
	@echo "*** ${GREEN}OK ${NC}***"
	@echo ""
	@echo "*** ${RED}help ${NC}***"
	${LIB} ${PY3} ${F} ${VERBOSE} --help
	@echo "*** ${GREEN}OK ${NC}***"
	@echo ""
	@echo "*** ${RED}short string, no randomness, show padding ${NC}***"	
	echo ${HELLO_WORLD} | ${LIB} ${PY3} ${F} ${VERBOSE} -R --mode encrypt ${PWD} > encrypt.out
	hexdump -C encrypt.out	
	cat encrypt.out |  ${LIB} ${PY3} ${F} ${VERBOSE} --mode decrypt -z ${PWD} > decrypt.out
	hexdump -C decrypt.out
	diff decrypt.out sc_1.ref
	@echo "*** ${GREEN}OK ${NC}***"
	@echo ""
	@echo "*** ${RED}short string, normal mode ${NC}***"
	echo ${HELLO_WORLD} > hello_world.txt
	cat hello_world.txt | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD} > encrypt.out
	hexdump -C encrypt.out	
	cat encrypt.out |  ${LIB} ${PY3} ${F} ${VERBOSE} --mode decrypt ${PWD} > decrypt.out
	hexdump -C decrypt.out
	diff decrypt.out hello_world.txt
	rm hello_world.txt
	@echo "*** ${GREEN}OK ${NC}***"
	@echo ""
	@echo "*** ${RED}longer text, no randomness, show padding ${NC}***"
	echo ${GETTYSBURG} | ${LIB} ${PY3} ${F} ${VERBOSE} -R --mode encrypt ${PWD} > encrypt.out
	hexdump -C encrypt.out
	cat encrypt.out |  ${LIB} ${PY3} ${F} ${VERBOSE} --mode decrypt -z ${PWD} > decrypt.out
	hexdump -C decrypt.out
	diff decrypt.out sc_2.ref
	@echo "*** ${GREEN}OK ${NC}***"
	@echo ""
	@echo "*** ${RED}longer text, multiple of the block size ${NC}***"
	cat getty-2.txt | ${LIB} ${PY3} ${F} ${VERBOSE} --mode encrypt ${PWD} > encrypt.out
	cat encrypt.out |  ${LIB} ${PY3} ${F} ${VERBOSE} --mode decrypt -z ${PWD} > decrypt.out
	hexdump -C decrypt.out
	diff decrypt.out sc_3.ref
	cat encrypt.out |  ${LIB} ${PY3} ${F} ${VERBOSE} --mode decrypt ${PWD} > decrypt.out
	diff decrypt.out getty-2.txt
	@echo "*** ${GREEN}OK ${NC}***"

clean:
	-rm encrypt.out decrypt.out hello_world.txt
	-rm -rf __pycache__ ../modules/__pycache__
	-rm hello-world.enc hungry-caterpiller.enc zero.in
