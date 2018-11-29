#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
char *list[30];

void init()
{
	setbuf(stdin,0);
	setbuf(stdout,0);
	setbuf(stderr,0);
	alarm(60);
}

int readn(char *str,int len)
{
	for(int i=0;i<len;i++)
	{
		read(0,str+i,1);
		if(*(str+i)=='\n') {*(str+i)=0;return i;}
	}
	return len;
}

int readint()
{
	char tmp[10];
	readn(tmp,8);
	return atoi(tmp);
}


int menu()
{
	puts("1.add");
	puts("2.delete");
	puts("3.show");
	puts("4.exit");
	printf(">>");
	return readint();
}
void add()
{
	for(int i =0;i<30;i++)
	{
		if(!list[i])
		{
			list[i]=malloc(0x20);
			printf("leave some message:");
			readn(list[i],0x10);
			puts("ok");
			return ;
		} 
	}
	puts("Full!");
	return;	
}

void dele()
{
	printf("index:");
	int idx = readint();
	if(idx<0||idx>=30) return;
	else
	{
		if(list[idx])
		{
			free(list[idx]);
			puts("ok");
			return ;
		}
	}
}

void show()
{
	printf("index:");
	int idx = readint();
	if(idx<0||idx>=30) return;
	else
	{
		if(list[idx])
		{
			puts(list[idx]);
			return ;
		}
	}
}
int  main()
{
	init();
	int c=0;
	while(1)
	{
		 c = menu();
		switch(c)
		{
			case 1:add();break;
			case 2:dele();break;
			case 3:show();break;
			case 4:puts("Bye!");exit(0);
			default:puts("Invalid");break;
		}
		
	}
}
