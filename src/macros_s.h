#ifndef MACROS_S_H
#define MACROS_S_H

#define RESTARTSAMPLE :.(:\
	lda #>_bwrt1:sta _ptr_wrt1+1:lda #>_bwrt2:sta _ptr_wrt2+1:lda #>_bwrt3:sta _ptr_wrt3+1:\
	lda #0:sta _ptr_wrt1:sta _ptr_wrt2:sta _ptr_wrt3:sta _position_low:sta _position_high:\
.)

#define LATCH_REG_NUMBER     sta via_porta:lda #$EE:sta via_pcr:lda #$CC: sta via_pcr
#define LATCH_REG_VALUE      sta via_porta:lda #$EC:sta via_pcr:lda #$CC: sta via_pcr

#endif