#!/usr/bin/env python3
import re, os
os.chdir(os.environ.get('GITHUB_WORKSPACE', '.') + '/kernel54')
with open('/tmp/ps_4_19.h') as f:
    cas = f.read()
with open('include/linux/power_supply.h') as f:
    current = f.read()
all_symbols = set(re.findall(r'\b(POWER_SUPPLY_[A-Z0-9_]+)\b', cas))
missing = [s for s in all_symbols if s not in current]
if not missing:
    print("No missing enums found.")
else:
    print(f"Found {len(missing)} missing enums. Injecting...")
    insertion = "\n\n/* Injected from 4.19 for cas_qcom compatibility */\n"
    for i, m in enumerate(missing):
        insertion += f"#ifndef {m}\n#define {m} (0x8000 + {i})\n#endif\n"
    last_endif = current.rfind('#endif')
    new_content = current[:last_endif] + insertion + current[last_endif:]
    with open('include/linux/power_supply.h', 'w') as f:
        f.write(new_content)
    print("Injected", len(missing), "symbols into include/linux/power_supply.h")