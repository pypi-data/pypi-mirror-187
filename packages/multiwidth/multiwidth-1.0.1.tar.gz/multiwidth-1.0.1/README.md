# Mixed Width

## About

This project is designed to enable the easy reading/writing of fixed-width files with variable widths. For example:

```
FOO     BAR     BAZ
Hello   World   SomeExtraLongString
```

In this case we have differing widths between the columns. This means we can't just specify a single width for the columns. This might not be much of an issue itself, just code in the differing widths and parse using that, however with things like console output we can't rely on a consistent width for cells, which is where Mixed Width comes in. To resolve this, it detects the start of cells by looking for location where spaces precede letters which line up across all lines of the files. Using this method we are able to parse files with unknown widths and convert them into either a list of lists, or a list of dictionaries where the keys are the header values.

## Examples

To use `multiwidth` for the most part it's the same as the built-in `json` module. This means that parsing some output takes the form of:

```python
import multiwidth

string_to_parse = """FOO     BAR     BAZ
Hello   World   SomeExtraLongString"""

data = multiwidth.loads(string_to_parse)

print(data)
# output:
# [['Hello', 'World', 'SomeExtraLongString']]
```

If preserving the headers is important, `output_json=True` can be added to the `loads` method:

```python
import multiwidth

string_to_parse = """FOO     BAR     BAZ
Hello   World   SomeExtraLongString"""

data = multiwidth.loads(string_to_parse, output_json=True)

print(data)
# output:
# [{'FOO': 'Hello', 'BAR': 'World', 'BAZ': 'SomeExtraLongString'}]
```

Each line will then be a dictionary with the header keys and their corresponding values

In addition, if the content is stored in a file, `multiwidth.load(<file_object>)` can be used. 

Finally, data can be output as well from multiwidth. 

```python
import multiwidth

headers = ['FOO', 'BAR', 'BAZ']
data = [['Hello', 'World', 'SomeExtraLongString']]

print(multiwidth.dumps(data, headers=headers))

# Output:
# FOO   BAR   BAZ
# Hello World SomeExtraLongString 
```

You can also control the spacing between columns with `cell_suffix='<your desired padding between columns>'`. For example:

```python
import multiwidth

headers = ['FOO', 'BAR', 'BAZ']
data = [['Hello', 'World', 'SomeExtraLongString']]

print(multiwidth.dumps(data, headers=headers, cell_suffix='   '))

# Output:
# FOO     BAR     BAZ
# Hello   World   SomeExtraLongString 
```

You can also dump JSON data by omitting the `headers` argument:

```python
import multiwidth

data = [{'FOO': 'Hello', 'BAR': 'World', 'BAZ': 'SomeExtraLongString'}]

print(multiwidth.dumps(data))

# Output:
# FOO   BAR   BAZ
# Hello World SomeExtraLongString
```

Finally, you can dump to a file with `dumps(<your file object>)`

## Usage

**load**

```python
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
```

**loads**

```python
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
```

**dump**

```python
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
```

**dumps**

```python
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
```

## License

Multiwidth is under the [MIT license](https://opensource.org/licenses/MIT).

## Contact

If you have any questions or concerns please reach out to me (John Carter) at [jfcarter2358@gmail.com](mailto:jfcarter2358@gmail.com)
