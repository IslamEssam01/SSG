- Still need to handle all edge cases and errors, as the program right now assumes that markdown is perfect and is written in a specific way.
For example 
    ```markdown
    # H1
    ## H2
    ### H3
    ```
    won't work as the program assumes that a heading must have an empty line after it.
- Add content and public folder as arguments to main.py instead of being hard coded.
- Refactoring of the code, as it is cluttered in directories
