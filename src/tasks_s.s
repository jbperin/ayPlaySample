
.zero


.text

#define LATCH_REG_NUMBER     sta via_porta:lda #$EE:sta via_pcr:lda #$CC: sta via_pcr
#define LATCH_REG_VALUE      sta via_porta:lda #$EC:sta via_pcr:lda #$CC: sta via_pcr

#define NB_SAMPLE 7440

TASK_4KHZ:
.(
   
    ldy     _position_low

    lda     (_ptr_wrt1), y
    tax
    and     #$F0
    lsr
    lsr
    lsr
    lsr 
    LATCH_REG_NUMBER
    txa
    and     #$0F
    LATCH_REG_VALUE

    ; lda chan1: LATCH_REG_NUMBER: lda signal1: LATCH_REG_VALUE
secval
    lda     (_ptr_wrt2), y
    tax
    and     #$F0
    lsr
    lsr
    lsr
    lsr 
    LATCH_REG_NUMBER
    txa
    and     #$0F
    LATCH_REG_VALUE

;    lda chan2: LATCH_REG_NUMBER: lda signal2: LATCH_REG_VALUE
thirval
    lda     (_ptr_wrt3), y
    tax
    and     #$F0
    lsr
    lsr
    lsr
    lsr 
    LATCH_REG_NUMBER
    txa
    and     #$0F
    LATCH_REG_VALUE
endval
;    lda chan3: LATCH_REG_NUMBER: lda signal3: LATCH_REG_VALUE


    inc     _position_low

    bne     skipNext256

        inc     _position_high
        inc     _ptr_wrt1+1
        inc     _ptr_wrt2+1
        inc     _ptr_wrt3+1


skipNext256

    lda     _position_low
    cmp     #<NB_SAMPLE 
    bne     skipResume

    lda     _position_high
    cmp     #>NB_SAMPLE
    bne     skipResume

restartsample
	lda #<_bwrt1
	sta _ptr_wrt1
	lda #>_bwrt1
	sta _ptr_wrt1+1

	lda #<_bwrt2
	sta _ptr_wrt2
	lda #>_bwrt2
	sta _ptr_wrt2+1

	lda #<_bwrt3
	sta _ptr_wrt3
	lda #>_bwrt3
	sta _ptr_wrt3+1

	lda #0
	sta _position_low
	sta _position_high

skipResume

task4kHz_done
.)
    rts




#define TASK_25Hz :.(:\
    pha:txa:pha:tya:pha:\
    jsr ReadKeyboard:\
    jsr detectKeyEvent:\
    pla:tay:pla:tax:pla:\
.)

