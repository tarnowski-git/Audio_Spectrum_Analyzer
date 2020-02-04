# Audio Spectrum Analyzer

Desktop GUI applications to show audio waveform and spectrogram which is visual representation of sound using the amplitude of the frequency components of the signal over time, using Python 3.7 with Tkinter graphic module.

Spectrograms are calculated from the time signal using a Fourier transform. The digital signal is divided into pieces corresponding to the analysis window. Calculations of the size of the frequency spectrum are made for each fragment. Each piece corresponds to a vertical image line, giving a picture of the measurement of energy and frequency amplitude for a specific time period. The spectra are then combined to create the image.

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

## [License](https://github.com/tarnowski-git/Audio_Spectrum_Analyzer/blob/master/LICENSE)

MIT © [Konrad Tarnowski](https://github.com/tarnowski-git)
