import subprocess
import hashlib
import pathlib
import shutil
import modules.constants as const


class WrongGameImageError(Exception):
    pass


def check_game_image():
    try:
        with open(const.ORIG_BIN, 'br') as image_fd:
            md5_digest = hashlib.file_digest(image_fd, 'md5').hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(
            f'Could not find original game image {const.ORIG_BIN.name} in {const.ORIG_BIN.parent}'
        ) from None

    if md5_digest != const.ORIG_BIN_MD5:
        raise WrongGameImageError('Game image does not have the expected MD5 hash, check README.md')


def extract_game_binaries():
    _create_game_idx()
    _extract_binaries()


def _create_game_idx():
    subprocess.run(
        [
            'java', '-jar', const.JPSXDEC,
            '-f', const.ORIG_BIN,
            '-x', const.GAME_IDX,
        ],
        check=True,
        capture_output=True,
    )


def _extract_binaries():
    for idx in const.GAME_FILES_IDX:
        subprocess.run(
            [
                'java', '-jar', const.JPSXDEC,
                '-x', const.GAME_IDX,
                '-i', idx,
                '-dir', const.BIN_DIR,
            ],
            check=True,
            capture_output=True,
        )
    pathlib.Path(const.DATA_FILE).rename(const.SRC_DATA_FILE)
    pathlib.Path(const.MAIN_EXE).rename(const.SRC_MAIN_EXE)


def compile_main():
    subprocess.run(
        [
            const.ARMIPS, const.MAIN_ASM,
        ],
        check=True,
        capture_output=True,
    )


def insert_files():
    shutil.copy(const.ORIG_BIN, const.PATCHED_BIN)
    for filepath in const.GAME_FILES:
        subprocess.run(
            [
                'wine', const.PSXINJECT,
                '-v', const.PATCHED_BIN,
                filepath.name, filepath,
            ],
            check=True,
            capture_output=True,
        )


def clean_up():
    to_delete = [const.GAME_IDX]
    to_delete += pathlib.Path(const.PROJECT_ROOT).glob('*.log')
    to_delete += const.FMVS + const.PATCHED_FMVS
    to_delete += const.GENERATED_ASM + const.SRC_GAME_FILES + const.GAME_FILES
    for f in to_delete:
        f.unlink()