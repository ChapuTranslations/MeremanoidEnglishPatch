; /// Character texture expansion routine ///
; Merge two ASCII textures into one for expansion
.org 0x8002d9b8
lbu		v0,0x0(a0)
lbu		v1,0x1(a0)
li		t2,0xb
addiu	v0,-0x80
addiu	v1,-0x80
mult	v0,t2
mflo	v0
mult	v1,t2
mflo	v1
la		t1,0x800a0448
addu	v0,t1
addu	v1,t1
la		t3,0x8002d70c
li		a0,0xa

tex_fetch_loop:
lbu		t1,0x0(v0)
lbu		t2,0x0(v1)
sll		t1,0x8
sll		t2,0x2
or		t1,t2
sh		t1,0x0(t3)
addiu	v0,0x1
addiu	v1,0x1
addiu	t3,0x2
bne		a0,r0,tex_fetch_loop
addiu	a0,-0x1

la		v0,0x8002d70c
jr		ra
nop

.org 0x8004f304
sltiu	v0,0x60

.org 0x8004f0f8
sltiu	v0,0x60

; Reduce vertical space between
; lines of text to 14 px so we
; can fit three lines per box
.org 0x8004f198
addiu	s3,0xe

; Fix for displaying cost of
; a stay at the inn
.org 0x80075ab4
addiu	v0,0x60
nop
sb		v0,0xb(s0)

.org 0x80075ac8
addiu	v0,0x60
nop
sb		v0,0xc(s0)

.org 0x80075adc
addiu	v0,0x60
nop
jal		0x8007a23c
sb		v0,0xd(s0)

.org 0x80075af4
addiu	v0,0x60
nop
sb		v0,0x29(s0)

.org 0x80075b08
addiu	v0,0x60
nop
sb		v0,0x2a(s0)

.org 0x80075b1c
addiu	v0,0x60
nop
sb		v0,0x2b(s0)

; Move battle camera options
; "Dynamic" and "Fixed" to the
; left and prevent them from
; overlapping
.org 0x80037904
li      s1,0x68

.org 0x80037954
addiu   s1,0x3c

; Fix file and chapter numbers
; on load/save screen
.org 0x80076f14
li      a2,0x80
li      a3,0x91

.org 0x80076f54
la      a1,0x80013f40

.org 0x80076f60
li      a2,0x80
addiu   a3,0x90

; Fix ailments in status menu
; so FRZ and PSN don't overlap
; each other or "Ailments"
.org 0x80037058
li      a2,0x9
addiu   a0,s0,0x3c

.org 0x80037088
li      a2,0xd

; /// BUY/SELL SCREEN ///
; Screen X coord for "PriceXCount"
.org 0x80070efc
li      v1,0x7e

.org 0x800716ac
addiu   a0,s1,0x79

; VRAM X coord for "X" in item list
.org 0x80070f04
li      v1,0x9c

; VRAM X pos for "Total"
.org 0x80070f0c
li      v1,0xc6

.org 0x80070f64
j       0x8002d724

; VRAM width for "Item"
.org 0x8002d724
li      v1,0x18
sh      v1,0x34(v0)

; VRAM width for "PriceXCount"
li      v1,0x47
sh      v1,0x3c(v0)

; VRAM width for "Total"
li      v1,0x1b
j       0x80070f6c
sh      v1,0x4c(v0)

; VRAM width for "Hold L2/R2: 10x"
.org 0x80070fe0
li      v1,0x60

; Screen X coord for "HeldXSell"
.org 0x800716bc
addiu   a0,s1,0x7e

; VRAM X coord for "HeldXSell"
.org 0x80070f9c
li      v1,0xb3

; /// TRICK/ATTACK/SPELL LEARN MESSAGE ///
; Tricks/Attacks
; Centre character name
.org 0x8004566c
move    s0,v0
nop
jal     len_minus_space
move    a0,s0
sll     v1,v0,0x1
addu    v1,v0
addiu   a0,v1,-0x3c
subu    a0,s2,a0

; Switch second and third lines
; anc centre second one
.org 0x800456b8
addiu   a1,s3,0x1c

.org 0x800456d8
addiu   a0,s2,0x12
addiu   a1,s3,0xe

; Determine if a skill is a
; trick or an attack to choose
; which message to show
; ("mastered"/"learned")
.org 0x800456e8
j       trick_or_attack
nop

; Spells
; Switch second and third lines
; and centre second one
.org 0x800361d8
li      a1,0x6c

.org 0x800361fc
li      a1,0x5e

.org 0x800361f8
li      a0,0x79

; Centre character name
.org 0x80036190
move    s1,v0
nop
jal     len_minus_space
move    a0,s1
sll     v1,v0,0x1
addu    v1,v0
li      a0,0xa0
subu    a0,v1

; Call strlen and subtract 1 to
; return value if last char of
; trick/spell is a blank space
.org 0x8004563c
jal     len_minus_space

.org 0x80036170
jal     len_minus_space

; Show "is escaping" with a preceding
; blank space or not depending on whether
; the character name has a blank space
; or not at the end
.org 0x8004a868
j       is_escaping
move    a0,s0
jal     0x80079d6c
move    a1,v0

; /// CHANGE SAVE FILE TEXT ///
; The PS1 BIOS only displays save file
; names in SJIS, up to 16 characters.
; Store "Meremanoid X" where X is
; the SJIS file number
.org 0x80077e74
j       save_file_name

.org 0x8002d740
len_minus_space:
addiu   sp,-0x14
sw      ra,0x10(sp)
jal     0x80079edc
li      t0,0x80
lbu     v1,-0x2(a0)
lw      ra,0x10(sp)
bne     t0,v1,ret_blank
nop
addiu   v0,-0x1
ret_blank:
jr      ra
addiu   sp,0x14

trick_or_attack:
; 0x8002d76c
la      v0,0x80010f1d
la      v1,0x8009adee
bge     s6,v1,is_trick
nop
addiu   v0,0xf
is_trick:
j       0x800456f0
nop

is_escaping:
; 0x8002d794
jal     0x80079edc
li      t0,0x80
addu    a0,s0,v0
lbu     v1,-0x1(a0)
la      v0,0x80011bf8
beq     t0,v1,trailing_blank
nop
addiu   v0,0xd
trailing_blank:
j       0x8004a870
move    a0,s0

save_file_name:
; 0x8002d7c0
lbu     v1,0x0(a2)
nop
addiu   v1,-0x41
sb      v1,0x17(a1)
jal     0x8007a23c
sb      r0,0x18(a1)
j       0x80077e7c
nop

; Fix for cut off chapter names
.org 0x80050920
li      v0,0xe0