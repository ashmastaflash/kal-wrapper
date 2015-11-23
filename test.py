import kalibrate
import pprint

pp = pprint.PrettyPrinter()

scanner = kalibrate.Kal("/usr/local/bin/kal")

#results = scanner.scan_band("GSM850", gain=45)

#pp.pprint(results)


target_channel = 232
gain = 45

results2 = scanner.scan_channel(target_channel, gain=gain)

pp.pprint(results2)
