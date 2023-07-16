### Getting Started
Ensure you have Python 3.9 or above. It should come along with pip, Python's package/dependency management system. 
After cloning this repository, here are the steps to run this app on macOS. We will utilize a `makefile` for ease of use.
1. Create a Python virtual environment in your working directory with `python -m venv env`. Consider why (here)[https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments]. Activate it with `source env/bin/activate`.
2. Run `make install` to install all the Python packages, like OpenAI and Pynecone.
3. Create an environment file, `.env`, to store your API key. In the code, I named mine `NEW_API_KEY`
4. Run `pc init` to initialize the Pynecone app.
5. Run `pc run` to run the app!

You're all set up! After running `pc run`, the app should be live at `localhost:3000`.