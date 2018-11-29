#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#define sp \
	__asm__(" push 	rax 	\n"\
			" xor 	rax,rax \n"\
			" jz 	opaque 	\n"\
			" add 	rsp,40 	\n"\
			"opaque:		\n"\
			" pop 	rax		\n");

char name[20] = "mozhucy's box";
char * R;
char map[200] = {8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 24, 25, 18, 19, 28, 29, 30, 31, 16, 17, 18, 19, 28, 29, 22, 23, 40, 41, 34, 35, 36, 37, 38, 47, 40, 41, 42, 43, 44, 45, 38, 39, 56, 57, 50, 59, 60, 53, 54, 55, 56, 57, 50, 51, 52, 61, 62, 55, 72, 73, 66, 75, 76, 69, 78, 79, 72, 73, 66, 95, 76, 77, 78, 71, 88, 89, 82, 83, 92, 85, 86, 87, 88, 89, 82, 83, 84, 85, 86, 87, 104, 105, 98, 99, 108, 109, 110, 111, 104, 97, 98, 99, 100, 101, 102, 103, 120, 121, 114, 123, 124, 125, 126, 127, 120, 113, 114, 123, 124, 125, 118, 119, 136, 129, 130, 139, 144, 141, 134, 143, 136, 137, 138, 139, 132, 141, 134, 135, 152, 145, 146, 147, 148, 149, 150, 151, 152, 145, 146, 147, 148, 157, 150, 151, 168, 161, 162, 163, 164, 173, 174, 175, 168, 161, 170, 171, 172, 173, 166, 167, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177, 178, 179, 180, 181, 182, 183};
struct player{
    int x;
    int y;
}player;
struct box{
    int x;
    int y;
}box;

struct player P;
struct box b1,b2;

void init_people_box(){
    P.x = 8;
    P.y = 5;
    b1.x = 5;
    b1.y = 2;
    b2.x = 8;
    b2.y = 7;
}
void welcome(){
    init_people_box();
    puts("       ...  ....'  .:i,`. ... I  ,,',.,..         ");
    puts("        ... ..',.  ''~^]`...l'}.:,:';`  ..        ");
    puts("       ...  ..^>.`?%B$$vi .'`'/Bb&BJ,.':.         ");
    puts("        ..  ..^>'fB$llb$( ^I`0%$ }o$~`:,.         ");
    puts("        .. . .``.$$-' /%d ..>$*, .p$1...          ");
    puts("           . .: ,$$; ,_WB.'`{$-  .p$j:.'          ");
    puts("       ..    .' .$$;.'~a& .+*p!  ~h$~.^           ");
    puts("          . ..`  @$j ,/8#I>($]I. z8d:''...        ");
    puts("       .'^'.:.`,'0$M:^/8$8%@$>;I.*$(I`i'..'..     ");
    puts("    .  ',;,',+Xk$&oB%,,[[,`-0}?.>&Wq}^]l~.'..     ");
    puts("       .^iIf$@kz~ .. `^'',,,`'`:`+rq&WX~!''..     ");
    puts("  .  . `,xWBx>`'`  .. '`.  .' `. `:;'Y*@wi'..     ");
    puts(" .'`,..:M$0,''.'' ''`.^!''.`' , ....^:!Q$M,'.,..  ");
    puts(".'.'``iM8{I'  .'lutY_`,YU}I'^''. '.`'',!18d^`^'.  ");
    puts(" '^^.i&$~:,.. ^-/>]}r!'{LbmZL-.`'. . '.^>-$o:...  ");
    puts(".'.^{$$x,. ...,}Lx-f}',(|uUnff,`   . '`  .@$C '.  ");
    puts(".. '$$u'... ..''.'.':`';[~,''.'.  ........f$B  '. ");
    puts(".  !$W,...... .. :!I:;;<|}i!; ... ........:$$+ `. ");
    puts(";  -$j ..'.. .'.,+,'!)|{~,:_/,`'. ........:o$n ,. ");
    puts("I '[$) ..... ..',+(1--_|ucL0[^'...........^M$n :. ");
    puts(":  -$]`..'..  ':!;}cqhaao#L+'''. '.......'`$$+ ^. ");
    puts(".. ~$Z.....   ..`>,'>_;^,!;.`'.... ... ..'u$&` '  ");
    puts(" . ^$$)..'.  ....^   .'``'  .'. ...... ..^$$r     ");
    puts(".`'^)$$(,.' .  .' .'....... .'' ....   .`}$a,'.   ");
    puts(" .,,.{@$['),`.'.'' .'.........'  .. _'>`{@Y,:^.   ");
    puts(".'. `:,Y@8['~.:^ .:` .......... ..`'+'l%@*:.'.'.  ");
    puts(" '.` .,i_aM@0.^^,'  `.......... ..,^`a@&c^ : ..   ");
    puts("       . ;'C$$$BZ. .`.       ^,  no$$W+   '..     ");
    puts(".  ..  .  ^U$M1LM@@$$$WhM@Wo%$$$@%zhB#' ..'..     ");
    puts("   ..     t%#`:.  . .-ju/(fj|>:   ^,x$b;-.'..     ");
    puts("..................................................");
    puts("..................................................");
    puts(".$$$:.....d$....-W$$$$$$*.._$$$$$$$$$$$~8$$$$$$$$$");
    puts(".$$8$*`...d$...$$k......$$......%$&.....8$W.......");
    puts(".$$zB$@...d$..I$a...............%$&.....8$W.......");
    puts(".$$z._$&:.d$..n$f...............%$&.....8$$$$$$$$^");
    puts(".$$z..,$$?d$..~$C.......,i`.....%$&.....8$W.......");
    puts(".$$z...I%$&$...$$Z......$$......%$&.....8$W.......");
    puts(".$$z.....>$$....u$$$$$$$c.......%$&.....8$W.......");
    puts("..................................................");
    puts("==================");
    puts("let's play a game!");
    puts("==================");
    R = (char *)malloc(1024);
    setbuf(stdin,NULL);
    setbuf(stdout,NULL);
    setbuf(stderr,NULL);
}
void catflag(){
    puts("you get it!");
    system("cat flag");
}
void boxW(struct box * p) {
    p->y -= 1;
}
void boxA(struct box * p) {
    p->x -= 1;
}
void boxS(struct box * p) {
    p->y += 1;
}
void boxD(struct box * p) {
    p->x += 1;
}
void D(){
    if(map[P.x + 1 + P.y * 16] != 8) {
        if(P.x + 1 == b1.x && P.y == b1.y) {
            if(map[(b1.x + 1) + b1.y*16] != 8) {
                boxD(&b1);
            } else {
                P.x -= 1;
            }
        } else if(P.x + 1 == b2.x && P.y == b2.y) {
            if(map[(b2.x + 1) + b2.y*16] != 8) {
                boxD(&b2);
            }
            else {
                P.x -= 1;
            }
        }
        P.x += 1;
    }
}
void W(){
    if(map[P.x + (P.y - 1) * 16] !=8 ) {
        if(P.x == b1.x && P.y - 1 == b1.y) {
            if(map[b1.x+ (b1.y - 1) * 16] != 8) {
                boxW(&b1);
            }
            else{
                P.y += 1;
            }
        } else if(P.x == b2.x && P.y - 1== b2.y) {
            if(map[b2.x + (b2.y - 1) * 16] != 8) {
                boxW(&b2);
            } 
            else {
                P.y += 1;
            }
        }
        P.y -= 1;
    }
}
void A(){
    if(map[P.x - 1 + P.y * 16]!=8) {
        if(P.x - 1 == b1.x && P.y == b1.y) {
            if(map[(b1.x - 1) + b1.y * 16] != 8) {
                boxA(&b1);
            }
            else {
                P.x += 1;
            }
        } else if(P.x - 1 == b2.x && P.y == b2.y) {
            if(map[(b2.x - 1) + b2.y * 16] != 8){
                boxA(&b2);
            }
            else{
                P.x += 1;
            }
        }
        P.x -= 1;
    }
}
void S(){
    if(map[P.x + (P.y + 1) * 16] != 8){
    if(P.x == b1.x && P.y + 1 == b1.y){
        if(map[b1.x + (b1.y + 1) * 16] != 8){
            boxS(&b1);
        }
        else{
            P.y -= 1;
        }
    }else if(P.x == b2.x && P.y + 1 == b2.y){
        if(map[b2.x + (b2.y + 1) * 16] != 8){
            boxS(&b2);
        }
        else{
            P.y -= 1;
        }
    }
    P.y += 1;
    }
    NULL;
}

void checkwin(){
    if(map[b1.x + b1.y*16]==20 && map[b2.x + b2.y * 16] == 20){
        puts("you get it");
        system("cat flag");
        exit(0);
    }
}
// void showmap(){
//     system("clear");
//     char m[200];
//     int i,j;
//     for(i=0;i<192;i++){
//         if(map[i] == 8){
//             m[i] = '#';
//         }
//         if(map[i] == 0){
//             m[i] = '.';
//         }
//         if(map[i] == 20){
//             m[i] = 'd';
//         }
//     }
//     m[P.x + P.y*16] = 'P';
//     m[b1.x + b1.y*16] = 'B';
//     m[b2.x + b2.y*16] = 'B';
//     puts("");
//     for(i=0;i<12;i++){
//         for(j = 0;j<16;j++){
//             printf("%c ",m[i*16 + j]);
//         }
//     puts("");
//     }
// }
void static __attribute__((constructor)) whereismap() {
    for(int i=0;i<192;i++){
        
        map[i] ^= i;
    }
    sp;
} 
int main(){
    welcome();
    read(0,R,1000);
    int len = strlen(R);
    int i = 0;
    char c;//wwaawaaawasssssssasddsdwddddwwwwwsaaawwdddsdwawddddwdssdsaa
        //WW44W444W45555555450050W0000WWWWW5444WW00050W4W0000W0550544
    for(i =0;i<1000;i++){
        // showmap();//debugƒƒßßßß
        // scanf("%c",&c);
        switch(R[i]){
            case '0':
                D();
                break;
            case '4':
                A();
                break;
            case '5':
                S();
                break;
            case 'W':
                W();
                break;
            default:
                puts("error!");
        }
        checkwin();
    }
    return 0;
}