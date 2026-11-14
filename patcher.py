#!/usr/bin/python3
import modules.build as build
import modules.script as script
import modules.visuals as visuals


def _check_game_image():
    print('Checking game image integrity')
    build.check_game_image()


def _extract_game_binaries():
    print('Extracting game binaries')
    build.extract_game_binaries()


def _create_translated_files():
    print('Creating translated script files')
    script.build_translation_asm()


def _compile():
    print('Compiling new assembly code')
    build.compile_main()


def _insert_font():
    print('Inserting new font')
    visuals.insert_font()


def _insert_files():
    print('Inserting modified files')
    build.insert_files()


def _insert_images():
    print('Inserting modified images')
    visuals.insert_images()


def _insert_fmv():
    print('Patching FMVs with subtitles')
    visuals.subtitle_fmvs()


def _clean_up():
    print('Cleaning up')
    build.clean_up()


def main():
    _check_game_image()
    _extract_game_binaries()
    _create_translated_files()
    _compile()
    _insert_font()
    _insert_images()
    _insert_files()
    _insert_fmv()
    _clean_up()


if __name__ == "__main__":
    main()