#include "macros_s.h"
#include "nbsample.h"
#include "config.h"

.zero

_ptr_wrt1       .dsb 2
_ptr_wrt2       .dsb 2
_ptr_wrt3       .dsb 2

_position_high  .dsb 1
_position_low   .dsb 1

.text

TASK_4KHZ:
.(
   
    ldy     _position_low

    lda     (_ptr_wrt1), y
    tax
    lsr
    lsr
    lsr
    lsr 
    LATCH_REG_NUMBER
    txa
    and     #$0F
    LATCH_REG_VALUE

secval
    lda     (_ptr_wrt2), y
    tax
    lsr
    lsr
    lsr
    lsr 
    LATCH_REG_NUMBER
    txa
    and     #$0F
    LATCH_REG_VALUE

thirval
    lda     (_ptr_wrt3), y
    tax
    lsr
    lsr
    lsr
    lsr 
    LATCH_REG_NUMBER
    txa
    and     #$0F
    LATCH_REG_VALUE
endval


    iny
    sty     _position_low    

    bne     skipNext256

        inc     _position_high
        inc     _ptr_wrt1+1
        inc     _ptr_wrt2+1
        inc     _ptr_wrt3+1


skipNext256

    cpy     #<NB_SAMPLE 
    bne     skipRestart

    lda     _position_high
    cmp     #>NB_SAMPLE
    bne     skipRestart

    RESTARTSAMPLE

skipRestart

task4kHz_done
.)
    rts

#ifdef USE_KEYBOARD_INTERRUPT
#define TASK_25Hz :.(:\
    jsr ReadKeyboard:\
    jsr detectKeyEvent:\
.)
#endif //USE_KEYBOARD_INTERRUPT


