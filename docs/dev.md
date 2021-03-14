# Developer Documentation

## Running the application

### Step 1 - PostgreSQL

Before running this application locally, you will need to set up a PostgreSQL database. If you have installed [PostgreSQL](https://www.postgresql.org/) already, be sure to run these commands:

```bash
$ psql
$ CREATE DATABASE youtubeify;
```

This will set up the database needed to run this application.

In the [config.py](https://github.com/umar-hasan/youtubeify/blob/main/app/config.py) file in the app folder, be sure to change the value of ```SQLALCHEMY_DATABASE_URI``` to ```'postgres:///youtubeify'```

### Step 2 - YouTube and Spotify API Information

This app relies on the YouTube and Spotify APIs, so you must retrieve API keys and credentials from both the Google and Spotify developer consoles. Check out these links for more information:

###### YouTube

* [Setting up YouTube OAuth 2.0 Credentials](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#creatingcred)

###### Spotify

* [Registering an Application](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app)

Once you have set up your YouTube and Spotify API credentials, be sure to set them up such that both the [YouTube](https://github.com/umar-hasan/youtubeify/blob/main/app/ytube/__init__.py) and [Spotify](https://github.com/umar-hasan/youtubeify/blob/main/app/spotify/__init__.py) ```__init__.py``` files point to them.

### Step 3 - Installing Requirements

In this project's root directory, be sure to set up the virtual environment. For more information on how to do that, check out these links:

* [Creating a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
* [Activating a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)

Once you have your virtual environment set up, be sure to install the necessary requirements using

```bash
pip install -r requirements.txt
```

within the virtual environment.

### Step 4 - Running the Application

In the virtual environment, run these commands to run the app:

```bash
export FLASK_ENV=development
flask run
```

## Testing

After following all of the steps above, in the virtual environment directory, you can run all tests using this command:

```bash
python -m unittest discover test
```
