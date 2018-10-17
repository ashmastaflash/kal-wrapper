import decimal
import sanity


def options_string_builder(option_mapping, args):
    """Return arguments for CLI invocation of kal."""
    options_string = ""
    for option, flag in option_mapping.items():
        if option in args:
            options_string += str(" %s %s" % (flag, str(args[option])))
    return options_string


def build_kal_scan_band_string(kal_bin, band, args):
    """Return string for CLI invocation of kal, for band scan."""
    option_mapping = {"gain": "-g",
                      "device": "-d",
                      "error": "-e"}
    if not sanity.scan_band_is_valid(band):
        err_txt = "Unsupported band designation: %" % band
        raise ValueError(err_txt)
    base_string = "%s -v -s %s" % (kal_bin, band)
    base_string += options_string_builder(option_mapping, args)
    return(base_string)


def build_kal_scan_channel_string(kal_bin, channel, args):
    """Return string for CLI invocation of kal, for channel scan."""
    option_mapping = {"gain": "-g",
                      "device": "-d",
                      "error": "-e"}
    base_string = "%s -v -c %s" % (kal_bin, channel)
    base_string += options_string_builder(option_mapping, args)
    return(base_string)


def herz_me(val):
    """Return integer value for Hz, translated from (MHz|kHz|Hz)."""
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
    """Return integer for frequency."""
    result = 0
    if direction == "+":
        result = base + modifier
    elif direction == "-":
        result = base - modifier
    return(result)


def to_eng(num_in):
    """Return number in engineering notation."""
    x = decimal.Decimal(str(num_in))
    eng_not = x.normalize().to_eng_string()
    return(eng_not)


def determine_scan_band(kal_out):
    """Return band for scan results."""
    derived = extract_value_from_output(" Scanning for ", -3, kal_out)
    if derived is None:
        return "NotFound"
    else:
        return derived


def determine_device(kal_out):
    """Extract and return device from scan results."""
    device = ""
    while device == "":
        for line in kal_out.splitlines():
            if "Using device " in line:
                device = str(line.split(' ', 2)[-1])
        if device == "":
            device = None
    return device


def determine_scan_gain(kal_out):
    """Return gain from scan results."""
    return(extract_value_from_output("Setting gain: ", 2, kal_out))


def determine_sample_rate(kal_out):
    """Return sample rate from scan results."""
    return(extract_value_from_output("Exact sample rate", -2, kal_out))


def extract_value_from_output(canary, split_offset, kal_out):
    """Return value parsed from output.

    Args:
        canary(str): This string must exist in the target line.
        split_offset(int): Split offset for target value in string.
        kal_out(int): Output from kal.
    """
    retval = ""
    while retval == "":
        for line in kal_out.splitlines():
            if canary in line:
                retval = str(line.split()[split_offset])
        if retval == "":
            retval = None
    return retval


def determine_avg_absolute_error(kal_out):
    """Return average absolute error from kal output."""
    return extract_value_from_output("average absolute error: ",
                                     -2, kal_out)


def determine_chan_detect_threshold(kal_out):
    """Return channel detect threshold from kal output."""
    channel_detect_threshold = ""
    while channel_detect_threshold == "":
        for line in kal_out.splitlines():
            if "channel detect threshold: " in line:
                channel_detect_threshold = str(line.split()[-1])
        if channel_detect_threshold == "":
            print("Unable to parse sample rate")
            channel_detect_threshold = None
    return channel_detect_threshold


def determine_band_channel(kal_out):
    """Return band, channel, target frequency from kal output."""
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
    """Parse kal band scan output."""
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
    """Parse kal channel scan output."""
    scan_band, scan_channel, tgt_freq = determine_band_channel(kal_out)
    kal_data = {"device": determine_device(kal_out),
                "sample_rate": determine_sample_rate(kal_out),
                "gain": determine_scan_gain(kal_out),
                "band": scan_band,
                "channel": scan_channel,
                "frequency": tgt_freq,
                "avg_absolute_error": determine_avg_absolute_error(kal_out),
                "measurements" : get_measurements_from_kal_scan(kal_out),
                "raw_scan_result": kal_out}
    return kal_data

def get_measurements_from_kal_scan(kal_out):
    """Return a list of all measurements from kalibrate channel scan."""
    result = []
    for line in kal_out.splitlines():
        if "offset " in line:
            p_line = line.split(' ')
            result.append(p_line[-1])
    return result
