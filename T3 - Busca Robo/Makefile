# GNU Makefile
# Revisão: ago/2020

CC = gcc
CCFLAGS = -Wall -O3
LDFLAGS = 
TARGET =  runRobo

all: $(TARGET)

%.o: %.c
	$(CC) $(CCFLAGS) -c $<

%: %.o
	$(CC) $(LDFLAGS) $^ -o $@

runRobo: main.c ambiente.o
	$(CC) $(CCFLAGSOPMP) ambiente.o main.c -o $@ $(LDFLAGS)

help:
	@echo
	@echo
	@echo "####### Exemplo de Execução #######"
	
clean:
	rm -f *.o *~ $(TARGET)