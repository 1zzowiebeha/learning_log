# Learning Log

# note: environment is currently paused.

Learning Log is a project based on the code written for
Python Crash Course 3rd Ed. by Eric Matthes.

It includes an additional statistics module,
a way to track hours spent with learning topics,
more CRUD features, and various UI changes.

--
### (insert gifs here that demonstrate functionality)
--

# Deploy to platform.sh:

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
See OS specific installation processes here: https://docs.platform.sh/administration/cli.html

### Login to platform.sh from the project's root directory:
    platform login

### Create a new platform project:
    platform create

### Push the project to the cloud:
    platform push

### View your live project url:
    platform url
    

### Check that your production env is secure
    platform environment:ssh [-p|--project PROJECT] [-e|--environment ENVIRONMENT]
 
1. ssh into machine
2. run `python manage.py check --deploy`
3. add recommended settings to your settings file

**Note**: From this ssh connection, you can also create a superuser for the admin site if you have enabled the `ENABLE_ADMIN_SITE_IN_PROD` setting.

### Cleanup:
    platform project:delete [-p|--project PROJECT]
    
    
### Troubleshooting:
CLI reference:
https://docs.platform.sh/administration/cli/reference.html

Django deployment tutorial:
https://docs.platform.sh/guides/django.html

The Platform.sh CLI uses curl. If you use a VPN, curl will timeout unless you
fiddle with http_proxy.
https://stackoverflow.com/questions/45410336/http-requests-working-in-browser-postman-timeout-when-using-curl-or-python-clie
https://www.golinuxcloud.com/set-up-proxy-http-proxy-environment-variable/
