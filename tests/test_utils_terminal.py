import pytest
from utils import terminal_kali
from utils.colors import C


def test_digitar_quick(capsys):
    # should not raise and should write the given text
    terminal_kali.digitar("test-output", delay=0, cor=C.KALI_BRANCO, fim="", pausa_final=0)
    captured = capsys.readouterr()
    assert "test-output" in captured.out


def test_terminal_ls_and_cat(capsys):
    tk = terminal_kali.TerminalKali()

    # List home
    tk._cmd_ls([])
    out1 = capsys.readouterr().out
    assert ".hidden" in out1

    # Read a hidden file
    tk._cmd_cat(["~/.hidden"])
    out2 = capsys.readouterr().out
    assert "arquivo oculto" in out2 or "[arquivo oculto]" in out2


def test_scp_error_and_success(capsys):
    tk = terminal_kali.TerminalKali()

    # existing file
    tk._cmd_scp(["~/Private/.conversa_hotel_nobile.pdf", "exfil@drop:~/"])
    out = capsys.readouterr().out
    assert "Transfer completed successfully" in out or "Transfer completed" in out

    # missing file
    tk._cmd_scp(["~/Private/does_not_exist.txt", "exfil@drop:~/"])
    out2 = capsys.readouterr().out
    assert "No such file or directory" in out2
