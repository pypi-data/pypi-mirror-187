# pylint: disable=R0912,R0915,R0914

"""A Python module for reading/writing fixed-width files with variable column widths"""

from typing import List, Dict, Union
import io


def get_letter_locations(contents: str, padding: str = " ") -> List[int]:
    """Gets the locations of starting letters of words in a string

    Args:
        contents (str): String to get starting letter locations from
        padding (str, optional): Padding between columns. Defaults to " ".

    Returns:
        List[int]: Indices in the string of starting letters of words
    """

    lines = contents.split("\n")

    # Remove empty lines
    lines = [line for line in lines if len(line) > 0]

    max_length = 0
    letter_locations = []
    # Get all the locations of the first letter of a word
    for line in lines:
        line_letter_locations = []
        chars = list(line)
        first_flag = True
        for idx, char in enumerate(chars):
            # Is it checking for the beginning of a work and not a space
            if first_flag and char != padding:
                line_letter_locations.append(idx)
                first_flag = False
                continue
            # If it's a space then we want to look for the beginning of a word
            if char == padding:
                first_flag = True

        letter_locations.append(line_letter_locations)
        if len(line) > max_length:
            max_length = len(line)
    # Now that we have the letter locations we want to know which ones they all have in
    # common. Start by loading in the first line
    global_letter_locations = letter_locations[0]

    # We then loop through all the lines and only keep those that are in common
    for letter_location in letter_locations[1:]:
        global_letter_locations = set(global_letter_locations).intersection(
            letter_location
        )

    global_letter_locations = sorted(list(set(global_letter_locations)))
    global_letter_locations.append(max_length + 1)

    return global_letter_locations


def split(line: str) -> List[str]:
    """Splits a line of text into a list of characters.

    Args:
        line (str): Line of text to split.

    Returns:
        List[str]: List of characters that make up the line of text.
    """

    # Split the line into a list of characters
    output = list(line)
    return output


def process_line(line: str, widths: List[int]) -> List[str]:
    """Breaks a line apart into cell data according to cell widths.

    Args:
        line (str): Line of text to process.
        widths (List[int]): Widths of each column in the file.

    Returns:
        List: List of strings representing each cell's data.
    """

    char_idx = 0
    output = []

    # Loop through each cell's widths
    for width in widths:
        # grab all the characters from the cell
        data_buffer = line[char_idx : char_idx + width]
        char_idx += width
        # Remove trailing whitespace
        output.append(data_buffer.strip())

    return output


def loads(
    contents: str, padding: str = " ", header: bool = True, output_json: bool = False
) -> Union[List[List], List[Dict]]:
    """Takes a string of a fixed-width file and breaks it apart into the data contained.

    Args:
        contents (str): String fixed-width contents.
        padding (str, optional): Which character takes up the space to create the fixed
            width. Defaults to " ".
        header (bool, optional): Does the file contain a header. Defaults to True.
        output_json (bool, optional): Should a list of dictionaries be returned instead
            of a list of lists. Defaults to False. Requires that 'header' be set to
            True.

    Raises:
        Exception: 'output_json' is True but 'header' is False.

    Returns:
        List[List] | List[Dict]: Either a list of lists or a list of dictionaries that
            represent the extracted data
    """

    lines = contents.split("\n")

    # Remove empty lines
    lines = [line for line in lines if len(line) != 0]

    # Normalize lengths of lines
    lengths = [len(line) for line in lines]
    max_lengths = max(lengths)
    for idx in range(0, len(lines)):  # pylint: disable=C0200
        if lengths[idx] < max_lengths:
            delta = max_lengths - lengths[idx]
            lines[idx] += padding * delta

    # Get the widths of each cell
    # Make sure we use the data to find the widths
    # Because sometimes the headers have spaces in them
    # And that will cause parsing to be weird
    word_locations = get_letter_locations(contents, padding=padding)
    widths = [
        word_locations[i + 1] - word_locations[i]
        for i in range(0, len(word_locations) - 1)
    ]

    if header:
        # Grab the headers if applicable
        headers = process_line(lines[0], widths)
        lines = lines[1:]
    output = []

    # Check that we have a header when requesting JSON output
    # We need the header for the dictionary keys
    if output_json:
        if not header:
            raise Exception(
                "'output_json' requires a header and for 'header' to be set to True"
            )

    for line in lines:
        # Grab the cell data from each line
        data = process_line(line, widths)
        if output_json:
            # Convert to dictionary if applicable
            datum = {}
            for idx, header_key in enumerate(headers):
                datum[header_key] = data[idx]
            # Add dictionary to output
            output.append(datum)
            continue
        # Add list to output
        output.append(data)

    return output


def load(
    file_object: io.TextIOWrapper,
    padding: str = " ",
    header: bool = True,
    output_json: bool = False,
) -> Union[List[List], List[Dict]]:
    """Parse data from a file object

    Args:
        file_object (io.TextIOWrapper): File object to read from
        padding (str, optional): Which character takes up the space to create the fixed
            width. Defaults to " ".
        header (bool, optional): Does the file contain a header. Defaults to True.
        output_json (bool, optional): Should a list of dictionaries be returned instead
            of a list of lists. Defaults to False. Requires that 'header' be set to
            True.

    Returns:
        Union[List[List],List[Dict]]: Either a list of lists or a list of dictionaries that
            represent the extracted data
    """

    # Read in out file
    contents = file_object.read()

    # Process the file
    output = loads(contents, padding=padding, header=header, output_json=output_json)

    return output


def dumps(
    data: Union[List[List], List[Dict]],
    headers: List[str] = None,
    padding: str = " ",
    cell_suffix: str = " ",
) -> str:
    """Dumps a formatted table to a string

    Args:
        data (Union[List[List],List[Dict]]): List or dictionary data to format
        headers (List[str], optional): Headers to use with list data. Defaults to None.
        padding (str, optional): Character to use as padding between values. Defaults to
            ' '.
        cell_suffix (str, optional): String to use as the padding between columns.
            Defaults to ' '.

    Returns:
        str: Formatted table of input data
    """

    is_dict = False
    if headers is None:
        headers = []
    if isinstance(data[0], dict):
        headers = list(data[0].keys())
        is_dict = True

    widths = []
    if headers:
        widths = [len(key) for key in headers]
    else:
        widths = [len(val) for val in data[0]]

    if is_dict:
        for datum in data:
            for idx, key in enumerate(headers):
                if len(datum[key]) > widths[idx]:
                    widths[idx] = len(datum[key])
    else:
        for datum in data:
            for idx, element in enumerate(datum):
                if len(element) > widths[idx]:
                    widths[idx] = len(element)

    output = ""
    if is_dict:
        if headers:
            out_string = ""
            for idx, val in enumerate(headers):
                width = widths[idx]
                delta = width - len(val)
                out_string += val + (delta * padding) + cell_suffix
            output += out_string.strip() + "\n"
        for datum in data:
            out_string = ""
            for idx, val in enumerate(headers):
                datum_val = datum[val]
                width = widths[idx]
                delta = width - len(datum_val)
                out_string += datum_val + (delta * padding) + cell_suffix
            output += out_string.strip() + "\n"
    else:
        if headers:
            out_string = ""
            for idx, val in enumerate(headers):
                width = widths[idx]
                delta = width - len(val)
                out_string += val + (delta * padding) + cell_suffix
            output += out_string.strip() + "\n"
        for datum in data:
            out_string = ""
            for idx, datum_val in enumerate(datum):
                width = widths[idx]
                delta = width - len(datum_val)
                out_string += datum_val + (delta * padding) + cell_suffix
            output += out_string.strip() + "\n"

    return output


def dump(
    data: Union[List[List], List[Dict]],
    file_object: io.TextIOWrapper,
    headers: List[str] = None,
    padding: str = " ",
    cell_suffix: str = " ",
):
    """Dumps a formatted table to a file

    Args:
        data (Union[List[List],List[Dict]]): Data to dump to a file. If using JSON data
            then omit the `headers` argument
        file_object (io.TextIOWrapper): File object to write to
        headers (List[str], optional): Headers to use with list data. Defaults to None.
        padding (str, optional): Character to use as padding between values. Defaults to
            ' '.
        cell_suffix (str, optional): String to use as the padding between columns.
            Defaults to ' '.
    """
    output = dumps(data, headers=headers, padding=padding, cell_suffix=cell_suffix)

    file_object.write(output)
