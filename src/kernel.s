
#include "via.h"
#include "tasks_s.s"

;; 4Khz
#define VIA_TIMER_DELAY_4KHZ	250    
#define VIA_TIMER_DELAY_8KHZ	125    

#define NB_IT_4KHZ		40

.zero

; Interruption Context Saving 
irq_A               .byt 0
irq_X               .byt 0
irq_Y               .byt 0

itCounter			.byt 0

.text

jmp_old_handler		.dsb 2

.dsb 256-(*&255)

irq_handler_4khz:
.(

;;	;Preserve registers 
	sta 	irq_A: stx 	irq_X: sty 	irq_Y
;;
	jsr TASK_4KHZ ;  TASK_4KHZ_4BITS ; 

	bit $304

 	dec itCounter: bne not100Hz 

	lda #160: sta itCounter ; 4000 / 25 Hz

	TASK_25Hz

not100Hz	
	;Restore Registers 
	lda irq_A: ldx 	irq_X: ldy 	irq_Y

	rti
.)




_kernelInit_4kHz:
.(
	sei

	; Save the old handler value
	lda $245
	sta jmp_old_handler+1
	lda $246
	sta jmp_old_handler+2


	lda 	#160 ; 4000 / 25 Hz
	sta		itCounter

	;; Set the VIA parameters (250 = 4Khz, )
	lda #<VIA_TIMER_DELAY_4KHZ
	sta $306 ;; via_t1ll
	lda #>VIA_TIMER_DELAY_4KHZ
	sta $307 ;; via_t1lh

	; Install our own handler
	lda #<irq_handler_4khz
	sta $245
	lda #>irq_handler_4khz
	sta $246


	RESTARTSAMPLE

    cli 
    rts
.)



_kernelEnd:
.(
	sei
	; Restore the old handler value
	lda jmp_old_handler+1
	sta $245
	lda jmp_old_handler+2
	sta $246

	;; Restore  VIA parameters
	lda #10
	sta via_t1ll
	lda #$27
	sta via_t1lh

	cli
    rts
.)

