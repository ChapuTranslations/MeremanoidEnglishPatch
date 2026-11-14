import pathlib
import re
import textwrap
import modules.constants as const


class OversizedDialogueBlockError(Exception):
    pass


def _get_lines_from(filepath):
    return pathlib.Path(filepath).read_text().splitlines()


def _pad_to_even_length(text):
    return text + ' ' if len(text) % 2 else text


def _format_line(translation: str) -> str:
    formatted_line = ''
    for chunk in const.CODE_PARSER.findall(translation):
        if chunk.startswith('{'):
            formatted_line += chunk
        else:
            chunk = _pad_to_even_length(chunk)
            formatted_line += chunk.replace('"', '\\"')
    return formatted_line


def build_translation_asm():
    _enemy_names()
    _exe_messages()
    _items()
    _dialogues()


def _enemy_names():
    translated_lines = _get_lines_from(const.ENEMY_NAMES)
    pos = const.RAM_OFFSET + const.ENEMY_NAMES_START_OFFSET
    with open(const.ENEMIES_ASM, 'w') as enemies_asm_fd:
        for idx, line in enumerate(translated_lines, start=1):
            _, name = line.split('|')
            print(const.NUM.format(idx), file=enemies_asm_fd)
            print(const.ORG.format(hex(pos)), file=enemies_asm_fd)
            print(const.STRING.format(_pad_to_even_length(name)), file=enemies_asm_fd)
            print('', file=enemies_asm_fd)
            pos += const.ENEMY_NAMES_STEP_SIZE


def _line_length(line):
    length = 0
    for chunk in const.CODE_PARSER.findall(line):
        if chunk.startswith('{'):
            length += 1 if chunk in const.ONE_BYTE_PLACEHOLDERS else 2
        else:
            length += len(chunk)
    return length


def _exe_messages():
    translated_lines = _get_lines_from(const.EXE_MESSAGES)
    cur_group = None
    cur_pos = -1
    with open(const.MESSAGES_ASM, 'w') as messages_asm_fd:
        for idx, line in enumerate(translated_lines, start=1):
            group, pos, ptrs, _, translation = line.split('|')

            # No translation? No problem!
            if not translation:
                continue

            print(const.NUM.format(idx), file=messages_asm_fd)
            lines = translation.split(const.NEWLINE_PLACEHOLDER)

            if group:
                if cur_group != group:
                    cur_group = group
                    cur_pos = int(pos, 16)
                ptrs = ptrs.split(',')

                for p in ptrs:
                    print(const.ORG.format(p), file=messages_asm_fd)
                    print(const.DW.format(hex(cur_pos)), file=messages_asm_fd)

                print(const.ORG.format(hex(cur_pos)), file=messages_asm_fd)
            else:
                print(const.ORG.format(pos), file=messages_asm_fd)

            formatted_lines = []
            for l in lines:
                length = _line_length(l)
                cur_pos += length
                if length % 2:
                    l = _pad_to_even_length(l)
                    cur_pos += 1
                formatted_lines.append(l.replace('"', '\\"'))

            cur_pos += len(lines) - 1
            formatted_line = const.NEWLINE_PLACEHOLDER.join(formatted_lines)
            print(const.STRING.format(formatted_line), file=messages_asm_fd)
            cur_pos += 1
            print('', file=messages_asm_fd)


def _items():
    # Main exe stores just item/spell names, max 16 chars
    translated_lines = _get_lines_from(const.EXE_ITEMS)
    with open(const.EXE_ITEMS_ASM, 'w') as exe_items_asm_fd:
        for idx, line in enumerate(translated_lines, start=1):
            pos, _, translation = line.split('|')
            print(const.NUM.format(idx), file=exe_items_asm_fd)
            print(const.ORG.format(pos), file=exe_items_asm_fd)
            print(const.STRING.format(_format_line(translation)), file=exe_items_asm_fd)
            print('', file=exe_items_asm_fd)

    # Data file stores item/spell descriptions
    translated_lines = _get_lines_from(const.DATA_ITEMS)
    with open(const.DATA_ITEMS_ASM, 'w') as data_items_asm_fd:
        for idx, line in enumerate(translated_lines, start=1):
            pos, _, translation = line.split('|')
            formatted_line = _format_line(translation)
            print(const.NUM.format(idx), file=data_items_asm_fd)
            print(const.ORG.format(pos), file=data_items_asm_fd)
            print(const.STRING.format(formatted_line), file=data_items_asm_fd)
            print('', file=data_items_asm_fd)


def _get_dialogue_block_lengths():
    data_file_data = pathlib.Path(const.SRC_DATA_FILE).read_bytes()
    block_start_offsets = [block.start() for block in re.finditer(const.DIALOGUE_BLOCK_MAGIC_NUM, data_file_data)]
    block_start_offsets.append(const.LAST_DIALOGUE_BLOCK_OFFSET)
    block_start_offsets.sort()
    return {hex(start): end-start for start, end in zip(block_start_offsets[:-1], block_start_offsets[1:])}


def _format_byte_string(byte_string):
    return const.DB.format(','.join([f'0x{bb}' for bb in textwrap.wrap(byte_string, width=2)]))


def _build_dialogue_block_header(word_1, word_3, size):
    return _format_byte_string(word_1 + size.to_bytes(4, 'little').hex() + word_3)


def _build_dialogue_block_line(text, target=None):
    return {'text': text, 'target': target}


def _update_branch_offsets(jump_lines, line_offsets):
    for line in jump_lines:
        target_offset = line_offsets[line['target']].to_bytes(2, 'little').hex()
        line['text'] = _format_byte_string(line['text'][:8] + target_offset + line['text'][12:])


def _output_dialogues_asm(dialogue_blocks):
    with open(const.DIALOGUES_ASM, 'w') as dialogues_asm_fd:
        for offset, block in dialogue_blocks.items():
            # Skip the first four bytes of the header, they're the magic number
            print(const.ORG.format(hex(int(offset, 16) + 4)), file=dialogues_asm_fd)
            for line in block:
                print(line['text'], file=dialogues_asm_fd)


def _dialogues():
    translated_lines = _get_lines_from(const.DIALOGUES)
    block_lengths = _get_dialogue_block_lengths()
    new_blocks = dict()
    line_offsets = dict()
    cur_block = []
    cur_block_start = ''
    cur_block_size = -1
    jump_lines = []

    for line in sorted(translated_lines):
        idx, block_start, header, orig, translation = line.split('|')
        line_offsets[idx] = cur_block_size - const.DIALOGUE_BLOCK_HEADER_BYTE_SIZE

        if block_start and block_start != cur_block_start:
            # Block starts with a 16 byte header
            # First 4-byte word is a magic number we ignore
            # Then come three more words:
            # word 1, block size, word 3
            if cur_block_start:
                # Check if this block's translation fits
                if cur_block_size > block_lengths[cur_block_start]:
                    excess = hex(cur_block_size - block_lengths[cur_block_start])
                    raise OversizedDialogueBlockError(
                        f'Block {cur_block_start} exceeds max size of {hex(block_lengths[cur_block_start])} by {excess} bytes.'
                    )

                cur_block.insert(
                    0, _build_dialogue_block_line(
                        _build_dialogue_block_header(word_1,word_3, cur_block_size)
                    )
                )

                # Store current dialogue block
                new_blocks[cur_block_start] = cur_block

            # Start new block
            cur_block_start = block_start
            cur_block_size = const.DIALOGUE_BLOCK_HEADER_BYTE_SIZE
            cur_block = []
            word_1 = header[1:9]
            word_3 = header[17:-1]

        # Process translated line or just codes
        if translation:
            translation_size = 0
            temp_translation = []
            chunks = const.CODE_PARSER.findall(translation)
            # First chunk is the text processing code, we'll deal with that later
            for chunk in chunks[1:]:
                if chunk.startswith('{') and chunk != const.STAR_PLACEHOLDER:
                    # Intermediate codes like newlines and wait for button press
                    # are just ASCII chars
                    code_ascii = ''.join([f'{ord(c):2x}' for c in chunk[1:-1]])
                    temp_translation.append(_format_byte_string(code_ascii))
                    translation_size += len(chunk) - 2
                else:
                    # Actual text
                    chunk = _pad_to_even_length(chunk)
                    translation_size += len(chunk) if chunk != const.STAR_PLACEHOLDER else 2
                    temp_translation.append(const.STRINGN.format(chunk.replace('"', '\\"')))

            # Add one to length to account for 0x0 terminator byte
            translation_size += 1
            cur_block_size += translation_size
            translation_size = translation_size.to_bytes(2, 'little').hex()

            # Insert processing code with translation size
            temp_translation.insert(0, _format_byte_string(chunks[0][1:-1] + translation_size))

            # Code 0x6 is four bytes: 2 for code and 2 for translation size
            # Code 0x8 is six bytes: 2 for code, 2 for index, and 2 for translation size
            cur_block_size += 4 if chunks[0].startswith('{06') else 6

            # Lines with text are aligned to 4 bytes using 0x0 as padding
            # Add an extra 0x0 as line terminator
            padding_len = ((cur_block_size + 3) & const.ALIGNMENT_MASK) - cur_block_size
            temp_translation.append(_format_byte_string(bytes(padding_len + 1).hex()))
            temp_translation = '\n'.join(temp_translation)
            cur_block_size += padding_len

            cur_block.append(_build_dialogue_block_line(temp_translation))

        else:
            orig = orig[1:-1]

            # All 08 codes end with 0x01000000
            if orig.startswith('08'):
                orig += '01000000'
                line = _build_dialogue_block_line(_format_byte_string(orig))

            # Code 05 is a conditional branch to other line in the block
            # Store them to update the jump offset later
            elif orig.startswith('05'):
                orig, target_line = orig.split(':')
                line = _build_dialogue_block_line(orig, target_line)
                jump_lines.append(line)
            else:
                line = _build_dialogue_block_line(_format_byte_string(orig))

            cur_block.append(line)
            cur_block_size += len(orig) // 2

    # Add header and last line to last block
    cur_block.insert(0, _build_dialogue_block_line(_build_dialogue_block_header(word_1, word_3, cur_block_size)))
    new_blocks[cur_block_start] = cur_block

    # Now that we know the position of each line relative to the start of their block
    # we can calculate the new offsets for the 05 code branching instructions
    _update_branch_offsets(jump_lines, line_offsets)
    _output_dialogues_asm(new_blocks)