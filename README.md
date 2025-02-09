# SoHunt
The Social OSINT Tool, utilizing face recognition.
## Installation
> You need firefox installed

First, clone the repo.
```bash
git clone https://github.com/LavedenC1/SoHunt
```
Next, install all dependencies,
```bash
pip intall -r requirements.txt
```
> It is recommended to create a venv

Now you need to install geckodriver.
1. First go to the geckodriver [releases](https://github.com/mozilla/geckodriver/releases) on the github.
2. Download the binary suitable for your machine.
3. Then make it available globally `sudo mv geckodriver /usr/local/bin ` or depending on your PATH
## Usage
1.Put pictures of your target in the known folder
2. Run SoHunt
To run SoHunt, run
```bash
python main.py
```
> Make sure to use python 3
> Also only facebook is currently supported

Thank you, more features to come later.
