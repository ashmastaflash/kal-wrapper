import decimal
import sanity


def build_kal_scan_band_string(kal_bin, band, args):
    option_mapping = {"gain": "-g",
                      "device": "-d",
                      "error": "-e"}
    if not sanity.scan_band_is_valid(band):
        err_txt = "Unsupported band designation: %" % band
        raise ValueError(err_txt)
    base_string = "%s -v -s %s" % (kal_bin, band)
    for option, flag in option_mapping.items():
        if option in args:
            base_string += str(" %s %s" % (flag, str(args[option])))
    return(base_string)


def build_kal_scan_channel_string(kal_bin, channel, args):
    option_mapping = {"gain": "-g",
                      "device": "-d",
                      "error": "-e"}
    base_string = "%s -v -c %s" % (kal_bin, channel)
    for option, flag in option_mapping.items():
        if option in args:
            base_string += str(" %s %s" % (flag, str(args[option])))
    return(base_string)


def herz_me(val):
    result = 0
    if val.endswith("MHz"):
        stripped = val.replace("MHz", "")
        strip_fl = float(stripped)
        result = strip_fl * 1000000
    elif val.endswith("kHz"):
        stripped = val.replace("kHz", "")
        strip_fl = float(stripped)
        result = strip_fl * 1000
    elif val.endswith("Hz"):
        stripped = val.replace("Hz", "")
        result = float(stripped)
    return(result)


def determine_final_freq(base, direction, modifier):
    result = 0
    if direction == "+":
        result = base + modifier
    elif direction == "-":
        result = base - modifier
    return(result)


def to_eng(num_in):
    x = decimal.Decimal(str(num_in))
    eng_not = x.normalize().to_eng_string()
    return(eng_not)


def determine_scan_band(kal_out):
    band = ""
    while band == "":
        for line in kal_out.splitlines():
            if "kal: Scanning for " in line:
                band = line.split()[3]
        if band == "":
            band = None
    return band


def determine_device(kal_out):
    device = ""
    while device == "":
        for line in kal_out.splitlines():
            if "Using device " in line:
                device = str(line.split(' ', 2)[-1])
        if device == "":
            device = None
    return device


def determine_scan_gain(kal_out):
    gain = ""
    while gain == "":
        for line in kal_out.splitlines():
            if "Setting gain: " in line:
                gain = str(line.split()[2])
        if gain == "":
            gain = None
    return gain


def determine_sample_rate(kal_out):
    sample_rate = ""
    while sample_rate == "":
        for line in kal_out.splitlines():
            if "Exact sample rate" in line:
                sample_rate = str(line.split()[-2])
        if sample_rate == "":
            sample_rate = None
    return sample_rate


def determine_chan_detect_threshold(kal_out):
    channel_detect_threshold = ""
    while channel_detect_threshold == "":
        for line in kal_out.splitlines():
            if "channel detect threshold: " in line:
                channel_detect_threshold = str(line.split()[-1])
        if channel_detect_threshold == "":
            print "Unable to parse sample rate"
            channel_detect_threshold = None
    return channel_detect_threshold


def determine_band_channel(kal_out):
    band = ""
    channel = ""
    tgt_freq = ""
    while band == "":
        for line in kal_out.splitlines():
            if "Using " in line and " channel " in line:
                band = str(line.split()[1])
                channel = str(line.split()[3])
                tgt_freq = str(line.split()[4]).replace(
                    "(", "").replace(")", "")
        if band == "":
            band = None
    return(band, channel, tgt_freq)


def parse_kal_scan(kal_out):
    kal_data = []
    scan_band = determine_scan_band(kal_out)
    scan_gain = determine_scan_gain(kal_out)
    scan_device = determine_device(kal_out)
    sample_rate = determine_sample_rate(kal_out)
    chan_detect_threshold = determine_chan_detect_threshold(kal_out)
    for line in kal_out.splitlines():
        if "chan:" in line:
            p_line = line.split(' ')
            chan = str(p_line[1])
            modifier = str(p_line[3])
            power = str(p_line[5])
            mod_raw = str(p_line[4]).replace(')\tpower:', '')
            base_raw = str((p_line[2]).replace('(', ''))
            mod_freq = herz_me(mod_raw)
            base_freq = herz_me(base_raw)
            final_freq = to_eng(determine_final_freq(base_freq, modifier,
                                                     mod_freq))
            kal_run = {"channel": chan,
                       "base_freq": base_freq,
                       "mod_freq": mod_freq,
                       "modifier": modifier,
                       "final_freq": final_freq,
                       "power": power,
                       "band": scan_band,
                       "gain": scan_gain,
                       "device": scan_device,
                       "sample_rate": sample_rate,
                       "channel_detect_threshold": chan_detect_threshold}
            kal_data.append(kal_run.copy())
    return kal_data


def parse_kal_channel(kal_out):
    kal_data = []
    scan_gain = determine_scan_gain(kal_out)
    scan_device = determine_device(kal_out)
    sample_rate = determine_sample_rate(kal_out)
    scan_band, scan_channel, tgt_freq = determine_band_channel(kal_out)
    for line in kal_out.splitlines():
        if "offset " in line:
            p_line = line.split(' ')
            iteration = str(p_line[-2]).split(':')[0]
            offset = p_line[-1]
            measurement = {"iteration": iteration,
                           "offset": offset,
                           "device": scan_device,
                           "sample_rate": sample_rate,
                           "gain": scan_gain,
                           "band": scan_band,
                           "channel": scan_channel,
                           "frequency": tgt_freq}
            kal_data.append(measurement.copy())
    return kal_data
