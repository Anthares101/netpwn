VERSION = '1.4'

SHELL_STABILIZATION_METHODS = {
    'python': {
        'bash': """python -c 'import pty; pty.spawn("/bin/bash")'""",
        'sh': """python -c 'import pty; pty.spawn("/bin/sh")'"""
    },
    'python3': {
        'bash': """python3 -c 'import pty; pty.spawn("/bin/bash")'""",
        'sh': """python3 -c 'import pty; pty.spawn("/bin/sh")'"""
    },
    'script': {
        'bash': 'script -qc /bin/bash /dev/null',
        'sh': 'script -qc /bin/sh /dev/null'
    }
}
