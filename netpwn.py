#!/usr/bin/env python3

import os, threading
from argparse import Namespace
from pwnlib.log import install_default_handler, getLogger
from pwnlib.tubes.listen import listen
from services import (
    ListennerService,
    ParametersParserService,
    TerminalService
)

# Init pwntools stuff and safe terminal conf
terminal_service = TerminalService()
install_default_handler()
log = getLogger('pwnlib')

def handler(listenner: listen):
    while listenner.connected('recv'): pass
    listenner.shutdown('send')

    # Restore terminal conf and exit
    terminal_service.restore_tty()

    log.setLevel(1)
    log.info(f'Closed connection to {listenner.rhost} port {listenner.rport}')
    os._exit(0)


def main(args: Namespace):
    lport = args.lport
    no_pty = args.no_pty

    listenner_service = ListennerService(lport)
    listenner = listenner_service.prepare_listener()
    listenner.wait_for_connection()

    if(listenner_service.is_rev_shell(listenner) and listenner_service.can_upgrade_shell(listenner) and not no_pty):
        with log.progress('Trying to stabilize the shell...') as p:
            try:
                listenner_service.upgrade_shell(listenner)
                terminal_service.pty = True
                p.success('Shell stabilized!')
            except:
                p.failure('Shell stabilization not possible, a non pty shell will be provided')
           
    # Start handler to control the closing
    handler_thread = threading.Thread(target=handler, args=(listenner,))
    handler_thread.setDaemon(True)
    handler_thread.start()
    
    # Start interactive mode
    log.info('Switching to interactive mode')
    log.setLevel('error')
    if(terminal_service.pty):
        terminal_service.set_raw_mode()
        listenner.sendline(b'') # Make the prompt appear
    listenner.interactive()

if __name__ == '__main__':
    print('Netpwn  - A netcat listenner alternative\n')

    parameterParserService = ParametersParserService()
    args = parameterParserService.parse_params()

    try:
        main(args)
    except KeyboardInterrupt:
        log.failure('Interrupted')
    except Exception as error:
        log.failure(error.__str__())
