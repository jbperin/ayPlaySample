#include <lib.h>

unsigned short 			running;
extern unsigned char 	nbE_keybuf;


void keyPressed(unsigned char c){
	if (running != 0) running--;
}

void keyReleased(unsigned char c){
}

void lsys(){
	unsigned char c;
	while (nbE_keybuf != 0) {
		c=get_keyevent();
		if (c & 0x80){
			keyReleased (c & 0x7F);
		} else {
			keyPressed (c);
		}
	}
}

void main()
{
	int 	mode0;

    // Deactivate cursor and keyclick
    mode0 = peek(0x26A);poke(0x26A, (mode0 | 0x08) & 0xFE);

	ayInit();

	kernelInit_4kHz();

	for (running = 1; running; ) lsys();

	kernelEnd();

    // Reactivate cursor and keyclick
    poke(0x26A, mode0);

}

