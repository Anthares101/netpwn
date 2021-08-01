#!/usr/bin/env python3

import os, threading
from argparse import Namespace
from pwnlib.log import install_default_handler, getLogger
from pwnlib.tubes.listen import listen
from netpwn.services import (
    ListenerService,
    ParametersParserService,
    TerminalService
)


# Init pwntools stuff and safe terminal conf
terminal_service = TerminalService()
install_default_handler()
log = getLogger('pwnlib')

def handler(listener: listen):
    while listener.connected('recv'): pass
    listener.shutdown('send')

    # Restore terminal conf and exit
    terminal_service.restore_tty()

    log.setLevel(1)
    log.info(f'Closed connection to {listener.rhost} port {listener.rport}')
    os._exit(0)


def netpwn(args: Namespace):
    lport = args.lport
    no_pty = args.no_pty

    listener_service = ListenerService(lport)
    listener = listener_service.prepare_listener()
    listener.wait_for_connection()

    if(listener_service.is_rev_shell(listener) and listener_service.can_upgrade_shell(listener) and not no_pty):
        with log.progress('Trying to stabilize the shell...') as p:
            try:
                listener_service.upgrade_shell(listener)
                terminal_service.pty = True
                p.success('Shell stabilized!')
            except:
                p.failure('Shell stabilization not possible, a non pty shell will be provided')
           
    # Start handler to control the closing
    handler_thread = threading.Thread(target=handler, args=(listener,))
    handler_thread.setDaemon(True)
    handler_thread.start()
    
    # Start interactive mode
    log.info('Switching to interactive mode')
    log.setLevel('error')
    if(terminal_service.pty):
        terminal_service.set_raw_mode()
        listener.sendline(b'') # Make the prompt appear
    listener.interactive()
    
def main():
    print('Netpwn  - A netcat listener alternative\n')

    parameterParserService = ParametersParserService()
    args = parameterParserService.parse_params()

    try:
        netpwn(args)
    except KeyboardInterrupt:
        log.failure('Interrupted')
    except Exception as error:
        log.failure(error.__str__())

if __name__ == '__main__':
    main()
