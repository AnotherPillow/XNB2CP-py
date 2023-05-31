# XNB2CP-PY

A Python script to convert XNB files to Content Patcher Content Packs for Stardew Valley.

## Notes before use

- Currently windows only, this will change soon.
- When the instructions say `py`, this may be `python` or `python3` depending on your system and specific installation.

## Usage

1. Install Python 3.8 or higher.
2. Download the contents of this repository.
3. Run `py -m pip install requirements.txt` in the directory you downloaded the repository to.
4. Put your XNB mod in `input`, as if it was the content folder of the game. (e.g. `input/Content/Characters/Maru.xnb`)
5. Run `py main.py` in the directory you downloaded the repository to.
6. Modify the `manifest.json` file in `output` to your liking.
7. Move the contents of `output` to a folder in `Mods` in your Stardew Valley directory.

## Credits

- XNB unpacking is done using [xnbcli](https://github.com/leonblade/xnbcli) by [leonblade](https://github.com/leonblade), licensed under LGPL-3.0.