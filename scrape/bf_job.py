#!/usr/bin/env python3
"""One-shot: on Black Friday (Nov 27, 2026) or Cyber Monday (Nov 30, 2026) open a Claude session in this folder and have it
run BLACK-FRIDAY-CHECK.md. usage: bf_job.py [blackfriday|cybermonday]
Started by ~/Library/LaunchAgents/com.benmartel.bulkapparel-<which>.plist, which this script removes after it runs."""
import os, subprocess, datetime, sys
WHICH = sys.argv[1] if len(sys.argv) > 1 else "blackfriday"
NAME, DAY, TITLE = {"blackfriday": ("Black Friday", datetime.date(2026, 11, 27), "BF BULKAPPAREL"),
                    "cybermonday": ("Cyber Monday", datetime.date(2026, 11, 30), "CM BULKAPPAREL")}[WHICH]
PL = os.path.expanduser("~/Library/LaunchAgents/com.benmartel.bulkapparel-%s.plist" % WHICH)
RC = os.path.expanduser("~/.claude/skills/rc-session/open_rc_session.py")
ENV = dict(os.environ, PATH="/Applications/cmux.app/Contents/Resources/bin:/Users/a7-13-2024/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin")
for line in open(os.path.expanduser("~/.claude/.env")):
    if line.startswith("CMUX_SOCKET_PASSWORD="): ENV["CMUX_SOCKET_PASSWORD"] = line.split("=", 1)[1].strip().strip('"\'')
today = datetime.date.today()
print(datetime.datetime.now().isoformat(), WHICH, "fired")
if today < DAY: print("too early, doing nothing"); sys.exit(0)
PROMPT = ("Scheduled job, set by Ben on Nov 18, 2026: today is the %s check. Read BLACK-FRIDAY-CHECK.md in this folder "
          "and carry it out start to finish without asking anything. It ends with a text to Ben through remind --text.") % NAME
r = subprocess.run(["/usr/bin/python3", RC, "/Users/a7-13-2024/projects/bulkapparel-vis", "--prompt", PROMPT, "--title", TITLE],
                   env=ENV, capture_output=True, text=True, timeout=600)
print(r.stdout, r.stderr)
if r.returncode != 0:
    subprocess.run(["remind", "--text", (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M"),
                    "BulkApparel %s check could not start" % NAME, "The Mac could not open the session. Ask Claude to run it by hand."],
                   env=ENV, cwd="/Users/a7-13-2024/projects/bulkapparel-vis")
subprocess.run(["launchctl", "unload", PL]); 
try: os.remove(PL)
except OSError: pass
