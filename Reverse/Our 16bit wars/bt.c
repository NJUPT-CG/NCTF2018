#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char flag[128];
// bc2e3b4c2eb03258c5102bf9de77f57dddad9edb70c6c20febc01773e5d81947
// bc2e3b4c2eb03258c5102bf9de77f57dddad9edb70c6c20febc01773e5d81947
char buf[128];
int pos = 0;


void pre_order(int idx)
{
	if (idx >= 64) return;
	buf[pos++] = flag[idx];
	pre_order(2 * idx + 1);
	pre_order(2 * idx + 2);
}

void in_order(int idx)
{
	if (idx >= 64) return;
	in_order(2 * idx + 1);
	buf[pos++] = flag[idx];
	in_order(2 * idx + 2);
}

int main()
{
	puts("Input flag:");
	scanf("%64s", flag);
	pos = 0;
	pre_order(0);
	if (!strcmp(buf, "bcec8d7dcda25d91ed3e0b720cbb6cf202b09fedbc3e017774273ef5d5581794"))
	{
		memset(buf, 0, 128);
		pos = 0;
		in_order(0);
		if (!strcmp(buf, "7d8dcdcaed592e1dcb07e02c36bcb2f0bf9e0bdcb0e13777237e25fd48515974"))
		{
			printf("TQL! TQL! flag: nctf{%s}\n", flag);
			return 0;
		}
		puts("Emmmm.....");
		return 0;
	}
	puts("GG!");
	return 0;
}
