# System Monitor
A library to monitoring system.
# Install
```
pip3 install systemmonitor
```
# Using
## In another script
```python
from systemmonitor import systemmonitor

#  systemmonitor(interval=2, nosystemload=False, nomemoryusage=False, nodiskusage=False)
monitor = systemmonitor()

print(monitor.system_load())
print(monitor.memory_usage())
print(monitor.disk_usage())

#or you can use monitoring

monitor.run()

```
## In command line
```console
systemmonitor run
```

parameters:
```console
systemmonitor run --interval 1 --nosystemload False --nomemoryusage False --nodiskusage False
```