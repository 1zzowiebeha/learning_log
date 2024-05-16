
# Features:
Fully implement custom relative date filter based off of humanize's implementation.
Implement topic-specific statistic pages

# Performance/Security:
Download plotly.js and serve the file from the server.
  
  Rewrite the graphs to be in JS, and to take data from the server
    https://adamj.eu/tech/2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
    
  Alternatively, use JQuery and grab the data from a backend API.
    Probably the better approach.

Download bootstrap css/js bundles and serve the files from the server.

# Auth
Allow for case insensitive logins
If login credentials are incorrect, don't forget the "next" GET query
Implement password change
Implement user accounts, profile picture media
Implement profiles

Only allow internally-served JS to load.

# Testing
Increase testing coverage

# Security
Do more of the steps recommended in this article:
https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure

Limit file size uploads
Limit file extensions allowed to be uploaded
Throttle login attempts
Implement captcha for logins and registration

For maximum security, make sure database servers only accept connections from your application servers.

configure the web server that sits in front of Django to validate the host. It should respond with a static error page or ignore requests for incorrect hosts instead of forwarding the request to Django. This way you’ll avoid spurious errors in your Django logs (or emails if you have error reporting configured that way).

If you haven’t set up backups for your database, do it right now! (automatic backups)

In production, you must define a STATIC_ROOT directory where collectstatic will copy static files.

Media files are uploaded by your users. They’re untrusted! Make sure your web server never attempts to interpret them.

Make automatic backups for your media files.

implement caching
cache sessions
tune the template cache

set the following for your postgres user so that django doesn't set it for each request:
client_encoding: 'UTF8'
default_transaction_isolation: 'read committed'
timezone: America/Detroit (does pg store in UTC regardless? and convert to user timezone?)

what's a pg session?


CONN_MAX_AGE:
  The development server creates a new thread for each request it handles, negating the effect of persistent connections. Don’t enable this setting during development.

When Django establishes a connection to the database, it sets up appropriate parameters, depending on the backend being used. If you enable persistent connections, this setup is no longer repeated every request. If you modify parameters such as the connection’s isolation level or time zone, you should either restore Django’s defaults at the end of each request, force an appropriate value at the beginning of each request, or disable persistent connections.

If a connection is created in a long-running process, outside of Django’s request-response cycle, the connection will remain open until explicitly closed, or timeout occurs.


