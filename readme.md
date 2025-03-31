# About
This is an emulator of a theoretical CPU for educational purposes.
When my professor was provided a simplified machine language to
demonstrate how a CPU interprets instructions, I thought the best
way to understand the material was to build an emulator and actually
code in that simplified machine language.

The program steps through each step of the fetch, decode, and execute
cycle. For each opcode it prints the documentation for that opcode
before executing.
The CPU is memory mapped to a controller that draws on a canvas
using Python's turtle graphics.

The documentation to each opcode is in `simple_machine_language.py`.

# Usage

To see the program in action.
```sh
cd simple_machine_language_emulator
python driver.py no_user
```

To step through each CPU instruction by pressing enter.
```sh
cd simple_machine_language_emulator
python driver.py
```

All available arguments are listed in `driver.py`.

The CPU registers and initial memory are found in the `memory` and
`registers` file. Edit the `memory` file to change the program.
