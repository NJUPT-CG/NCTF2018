#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>  
#include<fcntl.h>
#include<string.h>

void  init()
{
  setbuf(stdin, 0);
  setbuf(stdout, 0);
  setbuf(stderr, 0);
  alarm(60);
}

int  readn(char *str,int len)
{	
	char buf[2];
	int i=0;
	for(i =0;i<len;i++)
	{	
		read(0,buf,1);
		if(buf[0]=='\n') {buf[0]=0; break;}
		else
		{
			*(str+i)=buf[0];
		}		
	}
	
	return i;
	
}

void vul()
{
	char a[10];
	int n = readn(a,256);
	if(n%8 != 0) exit(0);
	return ;
}

void func()
{
	vul();
	exit(0);
}
int main()
{
	func();
	system("/bin/sh");
}
