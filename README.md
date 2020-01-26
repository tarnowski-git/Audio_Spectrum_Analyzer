# Audio Spectrum Analyzer

Desktop GUI applications with Python to show audio waveform and spectrgram, which is visual representation of sound - the amplitude of the frequency components of the signal over time.

Displays the waveform with matplotlib...

## Demo

![spectograph](https://user-images.githubusercontent.com/34337622/73137360-6fc90980-4057-11ea-932e-db6941c66e16.gif)

## Technologies

-   Python 3.7
-   Tkinter graphic module
-   NumPy module
-   SciPy module
-   Pillow module
-   Matplotlib module

## Prerequisites

-   [Python](https://www.python.org/downloads/)
-   [pip](https://pip.pypa.io/en/stable/installing/)
-   [pipenv](https://pipenv.readthedocs.io/en/latest/install/#make-sure-you-ve-got-python-pip)

## Installation

-   [Clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) this repo to your local machine using:

```
$ git clone https://github.com/tarnowski-git/Audio_Spectrum_Analyzer.git
```

-   Setup your [local environment](https://thoughtbot.com/blog/how-to-manage-your-python-projects-with-pipenv):

```
# Spawn a shell with the virtualenv activated
$ pipenv shell

# Install dependencies
$ pipenv install

# Run script into local environment
$ pipenv run python spectrum_analyzer.py
```

-   Compile with Pyinstaller to exectutable file:

```
# Windows
pyinstaller --onefile --windowed spectrum_analyzer.py
```

## [License](https://github.com/tarnowski-git/Audio_Spectrum_Analyzer/blob/master/LICENSE.md)

MIT © [Konrad Tarnowski](https://github.com/tarnowski-git)
