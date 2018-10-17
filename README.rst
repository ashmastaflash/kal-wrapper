=========
kalibrate
=========
Python wrapper for Kalibrate.
-----------------------------


Returns scan data in structured format.


Example usage:

::

  import kalibrate
  scanner = kalibrate.Kal("/usr/local/bin/kal")
  # Scan a band
  band_results = scanner.scan_band("GSM850", gain=45)
  # Scan a channel
  channel_results = scanner.scan_channel("232", gain=45)


And what you get for scanning a band:

::

  [{'band': 'GSM-850',
  'base_freq': 869200000.0,
  'channel': '128',
  'channel_detect_threshold': '259970.196875',
  'device': '0: Generic RTL2832U OEM',
  'final_freq': '869175933',
  'gain': '45.0',
  'mod_freq': 24067.0,
  'modifier': '-',
  'power': '299318.41',
  'sample_rate': '270833.002142'},
  {'band': 'GSM-850',
  'base_freq': 890000000.0,
  'channel': '232',
  'channel_detect_threshold': '259970.196875',
  'device': '0: Generic RTL2832U OEM',
  'final_freq': '890022169',
  'gain': '45.0',
  'mod_freq': 22169.0,
  'modifier': '+',
  'power': '780303.16',
  'sample_rate': '270833.002142'}]


Channel scan results:

::

{"device": "0: Generic RTL2832U OEM",
 "channel": "232",
 "band": "GSM-850",
 "gain": "45.0",
 "sample_rate": "270833.002142",
 "frequency": "890MHz",
 "average_absolute_error": "-33.445",
 "measurements":
    ["29921.37",
     "29952.37",
     "29900.71"],
 "raw_scan_result": "ORIGINAL FULL SCAN BODY GOES HERE"}

Note: Kalibrate's output for this feature starts numbering with offset 1. This
abstraction starts at 0, because that's how Python numbers things. So you'll
find your measurement for the first offset labeled "offset 1:" in the original
output, and in channel_scan["measurements"][0] in the output of the channel
scan. This format is new in version 2 of this library, and is a breaking change
from the way v1 presented this information.
