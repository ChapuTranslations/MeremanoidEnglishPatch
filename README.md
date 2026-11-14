# "Meremanoid" English translation patch

This includes all the necessary code and assets to patch the game and translate it to English.
Patcher script is Linux only, but it should be *relatively* easy to replicate the same steps in a .bat in Windows.

## What you'll need:
*	Java, Wine, xdelta3, and Python >=3.11 installed on your system.
*	A copy of the game ("Meremanoid (Japan)"), with the .cue and both .bin files extracted in the "bin" folder.
*	MD5 for "Meremanoid (Japan).bin" should be 8f0b4d6ab425c634887cb35c05f39267

##	You'll also need the following executables in the "tools" folder:
*	[armips](https://github.com/Kingcom/armips)
*	[jpsxdec.jar](https://github.com/m35/jpsxdec) and jpsxdec-lib.jar
*	psxinject.exe (part of the [psximager suite](https://github.com/cebix/psximager))

Simply give run permissions to patcher.py and execute. If everything's in order, it'll create a patched .bin of the game in the bin folder, and you'll be able to play it in English.

##	About this patch:
Back in February '26 I found out about this game. It looked graphically charming (I have a soft spot for fully 3D JRPGS since FFVII) and I had read that the story was deep and nuanced. So, after toiling away in the assembler mines for a couple of weeks, I managed to craft a script dump and reinsertion pipeline, and the graphical changes to support a half-width font.

At this point I was certain I could finish the job, so I proceeded to post about the game on BlueSky to see if anyone was interested in translating it. Misty got in touch immediately, followed by Cargodin, who let me know she had some of the translation and graphics work already done from a previous script dump by another hacker. We assembled a team, and the rest is history.

"Meremanoid" is not a flawless game by any stretch. However, I find that its minor shortcomings are more than compensated for by its charm. The 2D art is simply amazing, the music is excellent, and the story (and, more importantly, the *themes*) is not only very well-written and enthralling, but also every bit as relevant today as it was when the game came out, if not more so.

I hope you who are reading this enjoy the game very much. And remember that you can do whatever you want with this code: fork it, study it, change it, use it to translate the game to other languages, whatever you want. Knowledge should be free. I was only able to learn ROM hacking thanks to the kindness of people who came before me and selflessly shared their wisdom.

No IA, LLM, MTL or other such nonsense was used in the production of this patch. Not for the translation, not for the graphics, not for the coding, not for anything.

### Credits
*   Cargodin - Translation
*	Chapu - Programming/hacking
*	misty - Editing/proofreading
*	Mr. Nobody - Graphics and video editing
*	Popipopess - Translation
*   Shentok - Translation

## Changelog:
###	v1.0:
*	Initial commit. The game is fully translated and playable with the code as it stands. No *known* bugs at the moment.