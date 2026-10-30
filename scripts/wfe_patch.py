#!/usr/bin/env python3
import sys

f = sys.argv[1]
with open(f, 'r') as fh:
    s = fh.read()

old = 'ENTRY(stext)\n\tbl\tpreserve_boot_args'
new = 'ENTRY(stext)\n\twfe\n\tb\t.\n\tbl\tpreserve_boot_args'

if old in s:
    s = s.replace(old, new, 1)
    with open(f, 'w') as fh:
        fh.write(s)
    print('WFE patch applied successfully')
else:
    print('ERROR: ENTRY(stext) pattern not found')
    sys.exit(1)
