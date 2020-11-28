# frogger
Simple logging system to timestamp entries and compute durations, originally for keeping track of hours during quarantine.

### Initialize the frog

Initialize or access a frog with a file name:
```buildoutcfg
import froggers as fro
frog = fro.Frogger('frogs/test_log.txt')
```

If the file does not yet exist, it will be created.  Otherwise the present contents of the frog will get loaded.

### Splish in

Clock in like this:

```buildoutcfg
frog.splish()
```

This will begin keeping track of time until a clock out.

### Splash out

Clock out like this, adding a note to summarize activities:

```
frog.splash('just testing the system')
```

This will calculate the amount of time spent between clock in and clock out, and post the note to the log file.  It wil also calculate the entire amound of time spend on that particular day.

### Discrete mode

Alternatively, the frog can be set up in discrete mode, to record discrete events without calculating the time in between.  

Initialize in discrete mode:

```buildoutcfg
import froggers as fro
frog = fro.Frogger('frogs/discrete_list.txt', discrete=True)
```

### Add an entry

Add an entry to the frog:

```buildoutcfg
frog.croak('buy apples today')
```

This will simply add a timestamped entry with no duration accounted for

### Enjoy!