#!/usr/bin/env python3
"""b.py open URL -> prints tab id | b.py js TAB 'code' | b.py text TAB [maxchars] | b.py go TAB URL | b.py close TAB"""
import sys, time, json
sys.path.insert(0, '/Users/a7-13-2024/.claude/skills/gmail-send')
import gmail_send as g
c = sys.argv[1]
if c == 'open':
    before = {t[0] for t in g.tabs()}
    g.osa('tell application "Google Chrome" to open location "%s"' % sys.argv[2])
    for _ in range(20):
        time.sleep(1)
        n = [t for t in g.tabs() if t[0] not in before]
        if n: print(n[0][0]); break
elif c == 'js': print(g.runjs(sys.argv[2], sys.argv[3]))
elif c == 'go':
    g.runjs(sys.argv[2], "location.href=%s; 'ok'" % json.dumps(sys.argv[3])); time.sleep(6)
    print(g.runjs(sys.argv[2], "document.title+' | '+location.href"))
elif c == 'text':
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6000
    print(g.runjs(sys.argv[2], "document.title+' | '+location.href+'\\n'+document.body.innerText.replace(/\\n\\s*\\n+/g,'\\n').slice(0,%d)" % n))
elif c == 'close': g.close_tab(sys.argv[2]); print('closed')
