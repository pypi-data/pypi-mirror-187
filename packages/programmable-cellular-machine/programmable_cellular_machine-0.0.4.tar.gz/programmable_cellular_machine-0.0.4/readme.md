# Программируемый клеточный автомат

Клеточный автомат, в котором можно задавать правила, которые будут применяться к области.

## Профилирование

```bash
# скорость
poetry run python -m cProfile -o profile.prof main.py
poetry run gprof2dot -f pstats profile.prof | dot -Tpng -o profile.png

# память
poetry run python -m memory_profiler main.py 
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/programmable-cellular-machine/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/programmable-cellular-machine>
