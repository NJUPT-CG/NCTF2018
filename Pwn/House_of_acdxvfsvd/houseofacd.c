#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

void initialize()
{
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}

void menu()
{
	puts("=========NCTF 2018==========");
	puts("1. Heap of Homura");
	puts("2. Heap of Cossack");
	puts("3. Heap of MozhuCY");
	puts("4. Read the secret file");
	puts("5. Exit");
	puts("Input your choice:");
}

int read_flag = 0;

void myread(int fd, char* buf, int size)
{
	char c;
	int i = 0;
	for (i = 0; i < size; i++)
	{
		read(fd, &c, 1);
		if (c == 0x0A)
		{
			return;
		}
		buf[i] = c;
	}
	buf[i] = 0;
}

void read_secret_file()
{
	if (read_flag)
	{
		puts("You have already read the secret!");
		return;
	}
	FILE* fp = fopen("flagg", "r");
	if (!fp)
	{
		puts("Environment GG... Please contact the administrator");
		exit(-1);
	}
	char buf[128];
	fgets(buf, 120, stdin);
	puts(buf);
	read_flag = 1;
}

char* homura_ptr,* cossack_ptr,* mozhucy_ptr;
int homura_flag, cossack_flag, mozhucy_flag;
int homura_free, cossack_free, mozhucy_free;
int homura_count=0;
void heap_menu()
{
	puts("1. Alloc");
	puts("2. Free");
	puts("3. Show");
	puts("Input your choice:");
}

void allocate(int people)
{
	char** buf_ptr;
	int* flag_ptr;
	int size;
	if (people == 1) // homura
	{
		buf_ptr = &homura_ptr;
		flag_ptr = &homura_flag;
		size = 0x208;
	}
	else if (people == 2) // cossack
	{
		buf_ptr = &cossack_ptr;
		flag_ptr = &cossack_flag;
		size = 0x608;
	}
	else if (people == 3) // mozhucy
	{
		buf_ptr = &mozhucy_ptr;
		flag_ptr = &mozhucy_flag;
		size = 0x408;
	}
	if (people == 1)
	{	
		if(homura_count<2 && homura_count>=0)
			{puts("Homura Tql! He can allocate multiple times!");homura_count++;}
		else{puts("No!Homura can not allocate any more");exit(0);}
	}
	else if (*flag_ptr)
	{
		puts("You have allocated!");
		return;
	}
	*buf_ptr = (char *)malloc(size);
	if (!*buf_ptr)
	{
		puts("WTF?");
		exit(-1);
	}
	puts("Input your content:");
	myread(0, *buf_ptr, size);
	*flag_ptr += 1;
	puts("200 OK!");
	return;
}

void free_heap(int people)
{
	char** buf_ptr;
	int* flag_ptr;
	if (people == 1) // homura
	{
		buf_ptr = &homura_ptr;
		flag_ptr = &homura_free;
	}
	else if (people == 2) // cossack
	{
		buf_ptr = &cossack_ptr;
		flag_ptr = &cossack_free;
	}
	else if (people == 3) // mozhucy
	{
		buf_ptr = &mozhucy_ptr;
		flag_ptr = &mozhucy_free;
	}
	if (people == 1)
	{	
		if(homura_count <= 0 || homura_count > 2){puts("???");exit(0);}
		else{puts("Homura tql! He can free multiple times!");homura_count--;}
	}
	else if (*flag_ptr)
	{
		puts("You have freed!");
		return;
	}
	free(*buf_ptr);
	*buf_ptr = 0;
	*flag_ptr += 1;
	puts("200 OK!");
	return;
}

void show_heap(int people)
{
	char** buf_ptr;
	int size = 0;
	if (people == 1) // homura
	{
		buf_ptr = &homura_ptr;
		size = 0x208;
	}
	else if (people == 2) // cossack
	{
		buf_ptr = &cossack_ptr;
		size = 0x608;
		
	}
	else if (people == 3) // mozhucy
	{
		buf_ptr = &mozhucy_ptr;
		size = 0x408;
	}
	if(*buf_ptr) puts(*buf_ptr);
	return;
}

void heap_operate(int people)
{
	int choice = 0;
	heap_menu();
	scanf("%d", &choice);
	getchar();
	switch (choice)
	{
		case 1:
			allocate(people);
			break;
		case 2:
			free_heap(people);
			break;
		case 3:
			show_heap(people);
			break;
		default:
			puts("Meow meow meow?");
			break;
	}
}

// malloc(homura)
// malloc(cossack)
// malloc(mozhucy)
// free(cossack)
// free(homura)
// malloc(homura)
// overflow cossack
// malloc(homura)
// read_file == malloc(io_file)
// free(homura)
// free(mozhucy)
// malloc(comment)

void comment()
{
	puts("Please leave some comment!");
	char * buf = (char *)malloc(0x808);
	myread(0, buf, 0x809);
	exit(0);
}

int main()
{
	initialize();
	int choice = 0;
	while (choice != 5)
	{
		menu();
		scanf("%d", &choice);
		getchar();
		switch (choice)
		{
			case 1:
				heap_operate(1);
				break;
			case 2:
				heap_operate(2);
				break;
			case 3:
				heap_operate(3);
				break;
			case 4:
				read_secret_file();
				break;
			case 5:
				puts("May the force be with you!");
				comment();
				return 0;
				break;
			default:
				puts("Meow meow meow?");
				break;
		}
	}
}
