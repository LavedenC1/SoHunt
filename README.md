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
pip3 install -r requirements.txt
```
> It is recommended to create a venv

Now you need to install geckodriver.
1. First go to the geckodriver [releases](https://github.com/mozilla/geckodriver/releases) on the github.
2. Download the binary suitable for your machine.
3. Then make it available globally `sudo mv geckodriver /usr/local/bin ` or depending on your PATH
## Usage
1. **Put pictures of your target in the known/ directory**
2. Run SoHunt
```bash
python3 main.py
```
> Make sure to use python 3
> Only Facebook, Google Images, and DuckDuckGo are currently supported
## Inside SoHunt
Get commands:
```
$ help
```
View options:
```
$ options
```
Start the OSINTing:
```
$ start
```
### Examples
To set the target's name
```
$ set target.name John Doe
```
Get the target's name:
```
$ get target.name
```
Start the scraping
```
$ start
```
<hr>
Thank you, more features to come later.