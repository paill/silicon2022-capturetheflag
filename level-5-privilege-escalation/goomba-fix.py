#! /usr/bin/python3
# goombafix.py - a script that clears the bash history on the goomba account since goombas can't stop typing passwords in to the command line...

def _clear_bash_history():
    try:
        with open("/home/goomba/.bash_history", "r+") as fh:
            if fh.read():
                fh.truncate(0)
            else:
                pass
    except:
        pass

if __name__ == "__main__":
    _clear_bash_history()
