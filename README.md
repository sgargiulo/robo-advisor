# robo-advisor

Issues requests to the [AlphaVantage Stock Market API](https://www.alphavantage.co/) in order to provide automated stock or cryptocurrency trading recommendations.

## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip

## Installation

Fork this repository under your own control, then clone or download the resulting repository onto your computer. Then navigate there from the command line:

```sh
cd robo-advisor
```

> NOTE: subsequent usage and testing commands assume you are running them from the repository's root directory.

## Environment Setup

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```
From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

```sh
pip install pandas
```

# Setup Continued

Before using or developing this application, take a moment to [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key) (e.g. "abc123").

After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

    ALPHAVANTAGE_API_KEY="abc123"

Don't worry, the ".env" has already been [ignored](/.gitignore) from version control for you!

> NOTE: this app will try to use a "demo" API key if this environment variables is not configured.


## Usage

Run the recommendation script:

```py
python app/robo_advisor.py
```
Enter stock symbol (ticker) and then hit enter 

If you enter in an invalid ticker you will be notified and have to run the script again



## [License](/LICENSE.md)