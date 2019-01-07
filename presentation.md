class: center, middle

# SIGTERM.

[live presentation](https://alonisser.github.io/abstractions-talk/) <br/>
[twitter](alonisser@twitter.com), [medium](https://medium.com/@alonisser/)

Currently at [zencity.io](https://zencity.io/). We help cities leverage AI to understand their citizen's needs.

---
# Every thing that has a beginning has an end
Some day, I will die.

--

Some day, everyone in this room would die. 

--

For about 130 millions of years dinosaurs ruled the earth. And approx 65 million years ago they all died.   
--

Everything in nature dies

---
# Every thing that has a beginning has an end

A famous philosopher once claimed via one of his literary figures the "God is dead". He is also dead 

--

Even this planet would die some day. In about 7.5 billion years, Earth would be absorbed by the our dying sun Sol turning into a red giant.
---

# Every thing that has a beginning has an end

So yes, even your software processes would die someday.
--

So why do we keep writing software ignoring this fact?

---
# The death of a process

Why a process might die?
* It might just finish and exit 

* It might exit on an error or unhandled exception

* It might be killed by orchestrator - A django worker under gunicorn for example, supervisor

* System might kill it - because of memory problems, reboot, or multiple other reasons

* A parent process death might trigger a child process death

* It might get some kind of kill signal from a user

Death might also involve a chain of those events: memory constraints hit by k8 might cause k8 to shutdown a docker container,
 which in turn would kill the running process
 
---
# The death of a process

What might we want to handle on a process death? 

--

* Say farewell and allow your self to grieve
* Review you life
* Make your wishes known

--

* Say farewell and allow your self to grieve: Stop receiving new connections, finish processing current requests
* Review you life: Cleanup Db connections. temp files, pid.
* Make your wishes known: Log clear message on exit reason, might save current state. 

---
# The death of a process: design considerations
So besides "knowing" when death is upon us, what other design considerations our apps need to handle Termination gracefully?

---
# Signals

the harbingers of the process death.

* Sigterm
* SigInt
* SigKill

There are multitude of others. Including, Stop execution, Debug, reload, etc
But handling is less standardized 
-- 
also Windows probably also does something (?)

---
# Signals

* SigInt: usually a ctrl-c on an interactive session
* SigTerm: The common process kill command - allows the process the catch it and handle it gracefully
* Sigkill: Commonly called kill 9, Just die now. Can't be catched. No cleanup for you
---

# Python handling

The first thing you'll probably bump into is the atexit module 
```python
import atexit
@atexit.register
def nice_cleanup():
    print('Clean stuff here')
```

Let's try this!
--
Oh
---
# Python handling - atexit
Turns out that **atexit** handles only regular exit from the process:
```python
raise SystemExit()
# Or:
sys.exit() # Which raises SystemExit with the exit code provided - defaults to zero

```
But does not handle signals
---
# Python handling - signals

Python has a different method to handle signals
```python
import signal
signal.signal(signal.SIGTERM, nice_cleanup)
```
---
# Python handling -signals

But this has caveats also
```python
# In an imported lib code
signal.signal(signal.SIGTERM, lib_cleanup)
# In our code
signal.signal(signal.SIGTERM, my_cleanup)
```
Care to guess what would happen on SIGTERM?
--
Turns outs that the last signal handler replaces the one before

¯\_(ツ)_/¯

---
# Python handling - signals
So the best practice seems to be
```python
def my_cleanup():
    # clean things
handlers = [my_cleanup]

def cleanup_handler():
    for handler in handlers:
        handler()
old_handler = signal.signal(signal.SIGTERM, cleanup_handler)
handlers.append(old_handler)

```
No, you can be sure that a lib won't break this chain
---
Also, you still might need to handle regular exit with atexit. 

Because:

signal != atexit


--

This is why we cannot have nice things

---
class: center, middle

#Open source rocks!

---

class: center, middle

#Thanks for listening!

---
