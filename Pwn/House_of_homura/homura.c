#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>  
#include<fcntl.h>
#include<string.h>
int su = 0xdeadbeef;
typedef struct note
{
	char *name;
	char * message;
}note;

note *list[20];
note *tmp;

void  init()
{
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  alarm(60);
}


void banner()
{
puts(" _   _  ____ _____ _____ ____   ___  _  ___  ");
puts("| \\ | |/ ___|_   _|  ___|___ \\ / _ \\/ |( _ ) ");
puts("|  \\| | |     | | | |_    __) | | | | |/ _ \\ ");
puts("| |\\  | |___  | | |  _|  / __/| |_| | | (_) |");
puts("|_| \\_|\\____| |_| |_|   |_____|\\___/|_|\\___/ ");
puts("=============================================");
puts("This is homura\'s notebook.");
puts("There may be some clues.");
puts("Good luck,have fun!");
puts("=============================================");
}



int readn(char *str,int len)
{
	for(int i =0;i<len;i++)
	{
		read(0,str+i,1);
		if(*(str+i)=='\n') {*(str+i)=0;return i;}		
	}
	
	return len;
	
}

int readint()
{
	char x[16];
	readn(x,16);
	return atoi(x);
}

int menu()
{
	puts("1.add.");
	puts("2.delete.");
	puts("3.modify.");
	puts("4.exit.");
	printf(">>");
	return readint();
}

void add()
{
	int i=0;
	for(i=0;i<15;i++)
	{
		if(!list[i])break;
	}
	if(i>=15)
	{
		puts("full!");
		return;
	}
	list[i] =(note *)malloc(sizeof(note));
	list[i]->name = (char *)malloc(0x10);
	printf("length of your name:");
	int nl = readint();
	if(nl>=0x10) nl = 0x10;
	printf("your name:");	
	readn(list[i]->name,nl);
	printf("size of your message:");
	int ml = readint();
	if(ml<=0x80 || ml >=0x1000) ml=0x80;
	list[i]->message = (char *)malloc(ml+0x10);
	printf("please leave your message:");
	readn(list[i]->message,ml);
	puts("Done!");	
	return ;
}


void delete()
{
	printf("index:");
	int x = readint();
	if(x<0 || x>=15)
	{
		puts("invalid");
		return;	 
	}
	else
	{	
		free(list[x]->name);
		free(list[x]->message);
		free(list[x]);
		list[x]=0;
	}
	puts("Done!");
	return ;
}

void more_edit()
{
if(su!=0xdeadbeef) return;		
else{	
	su=0;
	printf("index:");
	int x = readint();
	if(x<0 || x>=15)
	{
		puts("invalid");
		return;	 
	}
	if(list[x]) tmp = list[x];
	if(!tmp) return ;
	printf("modify your message>");
	char temp_str[0x28];
	memset(temp_str,0,0x28);	
	readn(temp_str,0x8);
	printf("Here you can modify once again!>");
	readn(temp_str+0x18,0x8);
	memcpy(tmp->message,temp_str,0x20);	
	puts("Done!");
}
}


void edit()
{
	printf("index:");
	int x = readint();
	if(x<0 || x>=15)
	{
		puts("invalid");
		return;	 
	}
	if(list[x]) tmp = list[x];
	if(!tmp) return ;
	printf("size:");
	int l = readint();
	if(l>strlen(tmp->message)) l = 0x10;
	printf("Hello %s you can modify your message >",tmp->name);
	readn(tmp->message,l);
	puts("Done!");
	
}

int main()
{
	init();
	banner();
while(1){
	int choice = menu();
	switch(choice)
	{
		case 1:add();break;
		case 2:delete();break;
		case 3:edit();break;
		case 4:puts("Bye");exit(0);
		case 5:more_edit();break;
		default:puts("invalid");break;
	}	
	}			
}
