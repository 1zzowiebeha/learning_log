# Learning Log

Learning Log is a project based on the code written in
Python Crash Course 3rd Ed. by Eric Matthes.

It includes an additional statistics module,
a way to track hours spent with learning topics,
more CRUD features, and UI improvements.

--
### (insert gifs here that demonstrate functionality)
--

# To deploy on platform.sh:

### Create a virtual environment:

    python -m venv <venv_name>

### Activate virtual env:
**Note**: to de-activate, type `deactivate`

* Linux: `source <venv_name>/bin/activate`

* CMD: `<venv_name>\Scripts\activate`

* Powershell: `<venv_name>Scripts\Activate.ps1`

### Install packages in requirements.txt via PIP:
**Note**: your current directory must be the root directory

    pip install -r requirements.txt

### Install the platform.sh CLI:
See OS specific command here: https://docs.platform.sh/administration/cli.html

### Login to platform.sh from the root directory:
    platform login

### Create a new platform project:
    platform create

### Push the project to the cloud:
    platform push

### View your project:
    platform url

### Cleanup:
    platform <project>:delete