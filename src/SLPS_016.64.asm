.Open "bin/src_SLPS_016.64", "bin/SLPS_016.64", 0x8000f800
.headersize 0x8000f800

.include "src/SLPS_016.64_code.asm"
.include "src/SLPS_016.64_messages.asm"
.include "src/SLPS_016.64_items.asm"
.include "src/SLPS_016.64_extra.asm"
.include "src/SLPS_016.64_enemies.asm"

.Close
