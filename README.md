# Django Http:BL

Provides a simple middleware class that checks the client's IP address against
the [Http:BL](https://www.projecthoneypot.org/httpbl.php) database. IP addresses
identified as threats will receive a HTTP 403 response.

## Usage

- Add `httpbl` to `INSTALLED_APPS`
- Insert `httpbl.middleware.HttpBlMiddleware` into `MIDDLEWARE_CLASSES`, preferably at the top so that it runs before everything else.
- Add a `HTTPBL_API_KEY` with your API key obtained from [Project Honey Pot](https://www.projecthoneypot.org)

## Optional settings

- `HTTPBL_THREAT_SCORE`: the threat score at which to consider an IP a threat. Defaults to `35`.
- `HTTPBL_THREAT_AGE`: the maximum age in days at which to consider an IP a threat. Defaults to `30`.
- `HTTPBL_CACHE_LIFETIME`: cache lifetime for results, in seconds. Only applies if you have a working cache backend. Defaults to `86400` (1 day).

## Testing

```
$ export HTTPBL_API_KEY=yourapikey
$ py.test
```
