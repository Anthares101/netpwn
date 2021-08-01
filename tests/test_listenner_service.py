import unittest
from netpwn.services import ListenerService
from pwnlib.tubes.remote import remote
from netpwn.config import SHELL_STABILIZATION_METHODS


class ListenerServiceTest(unittest.TestCase):
    lhost = '127.0.0.1'
    lport = 8080
    
    def test_prepare_listener(self):
        listener_service = ListenerService(self.lport)
        listener = listener_service.prepare_listener()
        remote(self.lhost, self.lport)
        
        self.assertTrue(listener.connected())
        listener.close()

    def test_can_upgrade_shell(self):
        listener_service = ListenerService(self.lport)
        listener = listener_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)
        remote_shell.sendline(b'$')

        self.assertTrue(listener_service.can_upgrade_shell(listener))

    def test_cannot_upgrade_shell(self):
        listener_service = ListenerService(self.lport)
        listener = listener_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)
        remote_shell.sendline(b'Microsoft Windows')

        self.assertFalse(listener_service.can_upgrade_shell(listener))
    
    def test_upgrade_shell(self):
        listener_service = ListenerService(self.lport)
        listener = listener_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)
        expected_commands = ['export HISTFILE=/dev/null', 'which python', 'which bash', 'python -c \'import pty; pty.spawn("/bin/bash")\'; exit', 'export HISTFILE=/dev/null', 'stty rows 38 columns 116', " alias ls='ls --color=auto'", 'export TERM=xterm', 'history -c']
        commands_executed = []

        # Mock listener a bit
        def mocked_sendline(x): 
            remote_shell.sendline(b'fake@fake:~$ /usr/bin/python /bin/bash')
            commands_executed.append(x.decode())
        listener.sendline = mocked_sendline

        listener_service.upgrade_shell(listener)
        listener.close()
        self.assertListEqual(commands_executed, expected_commands)
    
    def test_find_pty_spawn_vector(self):
        listener_service = ListenerService(self.lport)
        listener = listener_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)

        # Mock listener a bit
        def mocked_sendline(x): remote_shell.sendline(b'fake@fake:~$ /usr/bin/python /bin/bash')
        listener.sendline = mocked_sendline

        self.assertEqual(listener_service.find_pty_spawn_vector(listener), SHELL_STABILIZATION_METHODS['python']['bash'])
        listener.close()
    
    def test_find_pty_spawn_vector_error(self):
        listener_service = ListenerService(self.lport)
        listener = listener_service.prepare_listener()
        remote_shell = remote(self.lhost, self.lport)

        # Mock listener a bit
        def mocked_sendline(x): remote_shell.sendline(b'fake@fake:~$ ')
        listener.sendline = mocked_sendline

        self.assertRaises(Exception, listener_service.find_pty_spawn_vector, listener)
        listener.close()


if __name__ == '__main__':
    unittest.main()
