import pathlib
import subprocess
import modules.constants as const


def insert_font():
    font_data = pathlib.Path(const.FONT).read_bytes()

    with open(const.MAIN_EXE, 'r+b') as main_exe_fd:
        main_exe_fd.seek(const.FONT_INSERTION_ADDRESS)
        main_exe_fd.write(font_data)


def _get_tim_data_from_num(tim_num):
    return (pathlib.Path(const.IMAGES_DIR) / f'DATA.E2K[{tim_num}].tim').read_bytes()


def insert_images():
    with open(const.DATA_FILE, 'br+') as data_fd:
        for tim_num, positions in const.IMAGE_POSITIONS.items():
            tim_data = _get_tim_data_from_num(tim_num)
            for position in positions:
                data_fd.seek(position)
                data_fd.write(tim_data)


def _patch_fmvs():
    for fmv, diff, patched_fmv in zip(const.FMVS, const.FMV_DIFFS, const.PATCHED_FMVS):
        subprocess.run(
            [
                'xdelta3', '-d', '-f',
                '-s', fmv, diff, patched_fmv,
            ],
            check=True,
            capture_output=True,
        )


def _insert_patched_fmv():
    with open(const.PATCHED_BIN, 'br+') as bin_fd:
        for fmv, pos in zip(const.PATCHED_FMVS, const.FMV_POS):
            fmv_data = pathlib.Path(fmv).read_bytes()
            bin_fd.seek(pos)
            bin_fd.write(fmv_data)


def subtitle_fmvs():
    _patch_fmvs()
    _insert_patched_fmv()