.org 0x80077e64
addiu	a1,0x3e50

.org 0x80013e50
.sjis "Ｍｅｒｅｍａｎｏｉｄ　１"

.org 0x800c246c
.db 0x94,0x00

.org 0x800c2470
.db 0x93,0x00

.org 0x800c2474
.db 0x92,0x00

.org 0x800c2478
.db 0x91,0x00

.org 0x800c222c
.string " {RIGHT}"

; Modified hard-coded pointers
; "Nothing learned."
.org 0x80034064
la      v0,0x80011b49

.org 0x80034800
la      v0,0x80011b49

; "Cannot be used"
.org 0x80034384
la      v0,0x80011b62

; "due to petrification!"
.org 0x800343b0
la      v0,0x80011b71

; "Strongest"
.org 0x80035270
addiu   v0,0x1b82

; "(Two-handed)"
.org 0x80035964
addiu   v0,0x1b8d

; "Nothing equipped."
.org 0x80035c84
la      v0,0x80011b9a

; "Cannot be equipped!"
.org 0x80035ce8
la      v0,0x80011bad

; "Nothing acquired."
.org 0x800365e8
la      v0,0x80011bc2

; "Attack Style"
.org 0x800367e0
addiu   v0,0x1bd5

; "Sound"
.org 0x80037820
la      v0,0x80011be2

; "Battle Camera"
.org 0x800378d8
la      v0,0x80011be9

; "Can't get away!"
.org 0x8004aa1c
la      v0,0x80010e90

; "acquired!"
.org 0x800501d4
la      v0,0x80010ea1

; "YES NO"
.org 0x80077984
la      a0,0x80010e74

; "Ailments"
.org 0x8003701c
la      v0,0x80010eac

; "FRZ"
.org 0x8003706c
la      v0,0x80010eb5

; "PSN"
.org 0x800370b8
la      v0,0x80010ec8

.org 0x8003fac8
la      v0,0x80010ec8

; "CRS"
.org 0x8003f978
la      v0,0x80010ed0

; "HDCH"
.org 0x8003f9cc
la      v0,0x80010ed7

; "NUMB"
.org 0x8003fa20
la      v0,0x80010ee2

; "SLOW"
.org 0x8003fa74
la      v0,0x80010ef3

; "Start"
.org 0x80043644
la      v0,0x80010efa

; "Exit"
.org 0x80043694
la      v0,0x80010f01

; "None"
.org 0x80049460
la      v0,0x80010f06

; "spot" got replaced by null 0x0
.org 0x8004a85c
lui     a1,0x8001

.org 0x8004a864
addiu   a1,0xf0b

; "learned spell:"
.org 0x80036208
la      v0,0x80010f0e

; "Buy Sell..."
.org 0x80070e8c
la      a0,0x80013708

; "Select details..."
.org 0x80070ec8
la      a0,0x80013730

; "Hold L2/R2..."
.org 0x80070f80
la      a0,0x80013759

; "Select item..."
.org 0x80072b74
la      v0,0x8001376a

; "Go to this..."
.org 0x8007375c
la      a0,0x80013789

; "Stay Save..."
.org 0x800757c0
la      a0,0x800137aa

; "Details"
.org 0x80033764
la      v0,0x800c21c2

; Remove "ha" from sprintf string
.org 0x800c2232
.dh     0x0

.org 0x800c2336
.dh     0x0