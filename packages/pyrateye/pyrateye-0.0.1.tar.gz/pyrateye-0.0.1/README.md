# RatEye ported to Python

This is a port of the RatEye project to Python. The original project is written in C# and can be found [here](https://github.com/RatScanner/RatEye).

## Installation

`pip install pyrateye`

## Usage

```python
from pyrateye import RatEye
# TBD
```

## Development

### Setup

Clone and install the project:

```bash
git clone https://github.com/marmig0404/pyrateye.git
cd pyrateye
poetry install --with dev
```

Install RatEye C# project:

```bash
git clone https://github.com/RatScanner/RatEye.git
cd RatEye
msbuild .\RatEye.csproj /property:Configuration=Release
```
