!/bin/bash
curl -s https://github.com/arendst/Sonoff-Tasmota/releases/latest | cut -d\" -f2 | rev | cut -d/ -f1 | rev 2>/config/versionsonoffhtml.err