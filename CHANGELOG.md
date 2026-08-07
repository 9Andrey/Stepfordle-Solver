# Changelog

# 0.3.1-beta

Features:
> - Added titles to the user interface to make its use simpler.

Fixed bugs:
> - Added an if statement to ensure "divide by zero" error does not occur.
>
> - [.gitignore](.gitignore) file did not ignore temporary files created by the software, now fixed.

# 0.3.0-beta

Features:
> - Added `bestGuessGivenTargets(*already_guessed: tuple) -> list` to ensure easier usage of [logic_manager.py](managers/logic_manager.py) module.
> 
> - Added [main.py](main.py) functionality and updated [README.md](README.md) accordingly

Edits:
> - Corrected error in [CHANGELOG.md](CHANGELOG.md) in v0.2.1-pre where it said `logic_manager.py` instead of `gui_manager.py`

## 0.2.1-pre
_Closed Release_

Fixed bugs:
> - When clicking `-` or `+` in the UI, you could get the number lower than `min_value` or higher than `max_value`

Refactioring:
> - [gui_manager.py](managers/gui_manager.py) rewriten to make easier usage and changes.

## 0.2.0-pre
_Closed Release_

Features:
> - Added [gui_manager.py](managers/gui_manager.py) support using customtkinter.

Edits:
> - Updated [README.md](README.md) to explain usage of gui_manager.py.
> 
> - Updated [requirements.txt](requirements.txt) to add `customtkinter`.
>
> - Edited [CHANELOG.md](CHANGELOG.md) to add hyperlinks in markup.

## 0.1.1-pre
_Closed Release_

Refactioring:
> - Corrected a typo in [logic_manager.py](managers/logic_manager.py).
>
> - Updated `clearTempFolder()` from [image_manager.py](managers/image_manager.py).

Edits: 
> - Updated [README.md](README.md) to explain module usage.

## 0.1.0-pre 
_Closed Release_

Initial release:
> - UI not available.
>
> - Basic modules operational.

Features:
> - Image editor tools implemented.
>
> - Full Stepfordle Game logic and data gathering tools implemented.