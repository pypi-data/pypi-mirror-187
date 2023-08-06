# HealthCheck_Pinger

HealthCheck_Pinger is a small and simple Python package that contains class and decorator to easily ping HealthCheck (https://healthchecks.io/) server.

## Installation
```bash
pip install healthcheck-pinger
```
## How to use
Use it like this:
```python
from HealthCheck_Pinger import PingHC
#sends start healthcheck
ping = PingHC("your uuid here") #or PingHC("your uuid here","your server url here")
try:
    your_code
except:
    ping.failure
else:
    ping.success
```
or like this:
```python
from HealthCheck_Pinger import pingDecor
@pingDecor("your uuid here") #or uuid and server url
def your_function():
    your_code
```
## License
[MIT](https://github.com/Gregorek85/HealthCheck_Pinger/blob/main/LICENSE)