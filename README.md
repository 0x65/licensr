licensr
=======

Automatically adds common licenses to your source code files. The product
of a couple hours one summer friday while my other code was going through
qa/review.

Usage
-----
> andrew$ python licensr.py -h
> usage: licensr.py [-h] [-r] [-e REGEX] [-p PREAMBLE] path license
> 
> Adds common licenses to your source files.
> 
> positional arguments:
>   path         The path root
>   license      The license to add
> 
> optional arguments:
>   -h, --help   show this help message and exit
>   -r           Recursively traverse directories to add licenses
>   -e REGEX     Regex to specify to which files licenses are added
>   -p PREAMBLE  A preamble added before the license, either a filename or
>                string (for copyrights, etc.)
> 
> Valid values for `license`:
> ---------------------------
> <file>  - A file of your own choosing
> gpl3    - GNU General Public License (GPL), version 3
> lgpl3   - GNU Lesser General Public License (LGPL), version 3
> apache2 - Apache License, version 2.0
> mit - MIT License
> mpl2    - Mozilla Public License (MPL), version 2
> none    - No license is added

