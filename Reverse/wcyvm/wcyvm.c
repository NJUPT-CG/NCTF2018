#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define EAX 1 
#define EBX 2
#define ECX 3
#define EDX 4
#define ESP 5
#define EBP 6
#define EIP 7 
#define MOVI 8
#define POP 9
#define PUSH 10
#define GETC 11
#define PUTC 12
#define CMP 13
#define JMP 14
#define JNZ 15
#define JZ  16
#define INC 17
#define DEC 18
#define ADD 19
#define SUB 20
#define XOR 21
#define AND 22
#define OR 23
#define NOT 24
#define MOVR 25
#define LEA0 26 
#define LEA1 27
#define LEA2 28
#define MUL 29
#define RET 100

char name[10] = "WcyVM1";
//nctf{3e1ce77b70e4cb9941d6800aec022c813d03e70a274ba96c722fed72783dddac}
unsigned int flagenc[72] = {0x36d3,0x2aff,0x2acb,0x2b95,0x2b95,0x2b95,0x169f,0x186d,0x18d7,0x1611,0x18d7,0x2b95,0x2c23,0x2ca9,0x1611,0x1611,0x18d7,0x2aff,0x1849,0x18fb,0x2acb,0x2a71,0x1735,0x18d7,0x1611,0x2acb,0x15dd,0x18d7,0x2c23,0x169f,0x15dd,0x2b95,0x169f,0x156b,0x186d,0x2aff,0x1611,0x1611,0x15dd,0x2aff,0x2c23,0x2acb,0x15dd,0x15dd,0x186d,0x1849,0x2b95,0x156b,0x1735,0x18fb,0x18fb,0x2a71,0x2aff,0x1735,0x2c23,0x15dd,0x18d7,0x2a71,0x18d7,0x18d7,0x2c23,0x2aff,0x156b,0x2c23,0x169f,0x35af,0x2ca9,0x32b5,0x2aff,0x3039};

unsigned int seed = 0;
unsigned int code[100] = { MOVI  ,EAX,0,
							MOVI  ,ECX,70,
							JMP  ,21,
							PUSH ,EAX,
							POP , EBX,
							GETC ,
							PUSH ,EAX,
							PUSH,EBX,
							POP  ,EAX,
							INC  ,EAX,
							CMP  ,EAX,ECX,
							JNZ  ,8,
							MOVI ,EAX,0,
							MOVI ,ECX,71,
							JMP  ,70,
							PUSH , EAX,
							LEA0 ,EBX,EBP,
							MUL ,EAX,4,
							SUB , EBX,EAX,
							MOVR , EAX,EBX,
							LEA1 , EAX,EAX,
							MUL,EAX,110,
							ADD,EAX,99,
							XOR,EAX,116,
							ADD,EAX,102,
							LEA2,EBX,EAX,
							POP,EAX,
							INC  ,EAX,
							CMP  ,EAX,ECX,
							JNZ  ,34,
							RET};

void movi(unsigned int * reg , unsigned int ch, unsigned int ** index) {
	*reg = ch;
	*index += 3;
	return;
}

void movr(unsigned int * dest , unsigned int * src , unsigned int ** index) {
	* dest = (unsigned int)* src;
	* index += 3;
	return;
}

void lea0(unsigned int * dest , unsigned int * src , unsigned int ** index) {
	* dest = src;
	* index += 3;
	return;
}
void lea1(unsigned int * dest , unsigned int * src , unsigned int ** index) {
	*dest = *(unsigned int *)(*src);
	* index += 3;
	return;
}
void lea2(unsigned int * dest , unsigned int * src , unsigned int ** index) {
	*(unsigned int *)(*dest) = (*src);
	* index += 3;
	return;
}
void push(unsigned int * reg,unsigned int ** esp, unsigned int ** index){
	*esp -= 1;
	**esp = *reg;
	*index += 2;
}

void pop(unsigned int * reg,unsigned int ** esp, unsigned int ** index){
	*reg = **esp;
	*esp += 1;
	*index += 2;
}

void Getc(unsigned int * rax,unsigned int ** index){
	*rax = getchar();
	*index += 1;
	return;
}
void Putc(unsigned int * rax,unsigned int ** index){
	putchar(*rax);
	*index += 1;
	return;
}

void ippp(unsigned int ** index){
	*index += 1;
}

void jmp(unsigned int ** index,int w,unsigned int * base){
	*index = base + w;
}

void jz(unsigned int flag,unsigned ** index,unsigned w,unsigned int * base){
	if (flag & 128){
		*index = base + w;
	}
	else{
		*index += 2;
	}
}

void jnz(unsigned int flag,unsigned ** index,unsigned w,unsigned int * base){
	if (!(flag & 128)){
		*index = base + w;
	}
	else{
		*index += 2;
	}
}

void inc(unsigned int * reg,unsigned int ** index){
	*reg += 1;
	*index += 2;
}

void dec(unsigned int * reg,unsigned int ** index){
	*reg -= 1;
	*index += 2;
}

void cmp(unsigned int * flag,unsigned int * reg1,unsigned int * reg2,unsigned int ** index){
	* flag = 0;
	* flag |= (*reg1 == *reg2) ? 128 : 0;
	* flag |= (*reg2 < *reg1) ? 64 : 0 ;
	* flag |= (*reg1 < *reg2) ? 32 : 0 ;
	*index += 3;
	return;
}

void add(unsigned int * reg1,unsigned int reg2,unsigned int ** index){
	* reg1 += reg2;
	*index += 3;
	return;
}

void sub(unsigned int * reg1,unsigned int * reg2,unsigned int ** index){
	* reg1 -= *reg2;
	*index += 3;
	return;
}

void xor(unsigned int * reg1,unsigned int ch,unsigned int ** index){
	* reg1 ^= ch;
	*index += 3;
	return;
}

void and(unsigned int * reg1,unsigned int * reg2,unsigned int ** index){
	* reg1 &= *reg2;
	*index += 3;
	return;
}

void or(unsigned int * reg1,unsigned int * reg2,unsigned int ** index){
	* reg1 |= *reg2;
	*index += 3;
	return;
}

void mul(unsigned int * reg1,unsigned int ch,unsigned int ** index){
	* reg1 *= ch;
	*index += 3;
	return;
}
int check(unsigned int * ebp){
	int i;
	int flag = 0;
	for(i = 0;i < 70;i++){
		flag |= (flagenc[i] == *(ebp - 70 + i)) ? 0 : 1;
	}
	return !flag;
}
int vm() {
	unsigned int flag = 0;
	unsigned int * text = (unsigned int *)malloc(0x200);
	unsigned int * stack = (unsigned int *) malloc(0x500 * sizeof(unsigned int));
	// unsigned int * esp = (unsigned int *)(stack + 0x500);
	// unsigned int * ebp = (unsigned int *)(stack + 0x500);
	unsigned int * reg[6] = {0};//eax ebx ecx edx
	memcpy(text,code,sizeof(code));
	reg[0] = malloc(7*sizeof(unsigned int *));
	reg[1] = reg[0] + 1;
	reg[2] = reg[1] + 1;
	reg[3] = reg[2] + 1;
	reg[4] = (unsigned int *)(stack + 0x500); //esp
	reg[5] = (unsigned int *)(stack + 0x500); //ebp
	reg[6] = text;
	while(*reg[6]){
		switch((char)(*reg[6])){
			case MOVI:
				movi(reg[*(reg[6] + 1) - 1],*(reg[6] + 2),&reg[6]);
				break;
			case PUSH:
				push(reg[*(reg[6] + 1) - 1],&reg[4],&reg[6]);
				break;
			case POP:
				pop(reg[*(reg[6] + 1) - 1],&reg[4],&reg[6]);
				break;
			case GETC:
				Getc(reg[0],&reg[6]);
				break;
			case PUTC:
				Putc(reg[0],&reg[6]);
				break;
			case JMP:
				jmp(&reg[6],*(reg[6] + 1),text);
				break;
			case JNZ:
				jnz(flag,&reg[6],*(reg[6] + 1),text);
				break;
			case JZ:
				jz(flag,&reg[6],*(reg[6] + 1),text);
				break;
			case INC:
				inc(reg[*(reg[6] + 1) - 1],&reg[6]);
				break;
			case DEC:
				dec(reg[*(reg[6] + 1) - 1],&reg[6]);
				break;
			case CMP:
				cmp(&flag,reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case ADD:
				add(reg[*(reg[6] + 1) - 1],*(reg[6] + 2) ,&reg[6]);
				break;
			case SUB:
				sub(reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case XOR:
				xor(reg[*(reg[6] + 1) - 1],*(reg[6] + 2),&reg[6]);
				break;
			case OR:
				or(reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case AND:
				and(reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case MOVR:
				movr(reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case LEA0:
				lea0(reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case LEA1:
				lea1(reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case LEA2:
				lea2(reg[*(reg[6] + 1) - 1],reg[*(reg[6] + 2) - 1],&reg[6]);
				break;
			case MUL:
				mul(reg[*(reg[6] + 1) - 1],*(reg[6] + 2),&reg[6]);
				break;
			case RET:
				return check(reg[5]);
				break;
			default:
				ippp(&reg[6]);
				continue;
		}
	}
	return 1;
}

int main() {
	setbuf(stdin,NULL);
	setbuf(stdout,NULL);
	printf("This is a %s\nplz input your flag:",name);
	if(vm()){
		puts("flag is your input");
	}
	else{
		puts("didixingwei");
	}
	return 0;
}
