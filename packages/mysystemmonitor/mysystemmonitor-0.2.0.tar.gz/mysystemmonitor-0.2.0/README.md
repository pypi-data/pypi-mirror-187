# My System Monitor
A library to monitoring system.
# Install
```
pip3 install mysystemmonitor
```
# Using
## In another script
```python
from mysystemmonitor import mysystemmonitor

#  mysystemmonitor(interval=2, nosystemload=False, nomemoryusage=False, nodiskusage=False)
monitor = mysystemmonitor()

print(monitor.system_load())
print(monitor.memory_usage())
print(monitor.disk_usage())

#or you can use monitoring

monitor.run()

```
## In command line
```console
mysystemmonitor run
```

parameters:
```console
mysystemmonitor run --interval 1 --nosystemload False --nomemoryusage False --nodiskusage False
```