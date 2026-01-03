#!/usr/bin/env python3
import sys
import io
import contextlib
from utils import terminal_kali
from utils.colors import C

checks = []

# Test 1: digitar quick
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    terminal_kali.digitar("test-output", delay=0, cor=C.KALI_BRANCO, fim="", pausa_final=0)
out = buf.getvalue()
checks.append(("digitar quick", "test-output" in out))

# Test 2: ls and cat

try:
    tk = terminal_kali.TerminalKali()
except Exception as e:
    print('Failed to instantiate TerminalKali:', e)
    sys.exit(2)

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    tk._cmd_ls([])
out_ls = buf.getvalue()
checks.append(("ls home contains .hidden", ".hidden" in out_ls))

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    tk._cmd_cat(["~/.hidden"])
out_cat = buf.getvalue()
checks.append(("cat hidden contains arquivo oculto", ("arquivo oculto" in out_cat) or ("[arquivo oculto]" in out_cat)))

# Test 3: scp success and failure
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    tk._cmd_scp(["~/Private/.conversa_hotel_nobile.pdf", "exfil@drop:~/"])
out_scp = buf.getvalue()
checks.append(("scp existing transfer message", ("Transfer completed successfully" in out_scp) or ("Transfer completed" in out_scp)))

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    tk._cmd_scp(["~/Private/does_not_exist.txt", "exfil@drop:~/"])
out_scp2 = buf.getvalue()
checks.append(("scp missing file error", "No such file or directory" in out_scp2))

# Report
ok = True
for name, passed in checks:
    status = "OK" if passed else "FAIL"
    print(f"{name}: {status}")
    if not passed:
        ok = False

if not ok:
    print("Some checks failed.")
    sys.exit(2)

print("All compatibility checks passed.")
sys.exit(0)
