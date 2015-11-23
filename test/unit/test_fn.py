from kalibrate import fn

kal_scan_sample = """Found 1 device(s):
  0:  Generic RTL2832U OEM

Using device 0: Generic RTL2832U OEM
Found Rafael Micro R820T tuner
Exact sample rate is: 270833.002142 Hz
Setting gain: 45.0 dB
kal: Scanning for GSM-850 base stations.
channel detect threshold: 261365.030729
GSM-850:
	chan: 231 (889.8MHz + 22.127kHz)	power: 348914.01
	chan: 232 (890.0MHz + 23.989kHz)	power: 743611.97
	chan: 237 (891.0MHz - 27.715kHz)	power: 322386.85

"""

kal_freq_offset_sample = """Found 1 device(s):
  0:  Generic RTL2832U OEM

Using device 0: Generic RTL2832U OEM
Found Rafael Micro R820T tuner
Exact sample rate is: 270833.002142 Hz
Setting gain: 45.0 dB
kal: Calculating clock frequency offset.
Using GSM-850 channel 232 (890.0MHz)
	offset   1: 29921.37
	offset   2: 29952.37
	offset   3: 29900.71
	offset   4: 29889.35
	offset   5: 29808.76
	offset   6: 29789.13
	offset   7: 29777.77
	offset   8: 29749.87
	offset   9: 29827.35
	offset  10: 29836.65
	offset  11: 29882.11
	offset  12: 29808.76
	offset  13: 29813.92
	offset  14: 29771.56
	offset  15: 29763.30
	offset  16: 29749.87
	offset  17: 29672.38
	offset  18: 29870.74
	offset  19: 29750.90
	offset  20: 29849.05
	offset  21: 29834.59
	offset  22: 29790.16
	offset  23: 29776.73
	offset  24: 29733.34
	offset  25: 29911.04
	offset  26: 29790.16
	offset  27: 29708.54
	offset  28: 29732.31
	offset  29: 29845.96
	offset  30: 29786.03
	offset  31: 29665.15
	offset  32: 29701.31
	offset  33: 29773.63
	offset  34: 29740.57
	offset  35: 29822.19
	offset  36: 29768.46
	offset  37: 29874.88
	offset  38: 29750.90
	offset  39: 29738.50
	offset  40: 29713.71
	offset  41: 29743.67
	offset  42: 29758.13
	offset  43: 29679.61
	offset  44: 29740.57
	offset  45: 29796.36
	offset  46: 29709.58
	offset  47: 29690.98
	offset  48: 29833.56
	offset  49: 29727.14
	offset  50: 29635.19
	offset  51: 29804.63
	offset  52: 29738.50
	offset  53: 29942.03
	offset  54: 29790.16
	offset  55: 29737.47
	offset  56: 29713.71
	offset  57: 29763.30
	offset  58: 29832.52
	offset  59: 29862.48
	offset  60: 29707.51
	offset  61: 29687.88
	offset  62: 29671.35
	offset  63: 29620.73
	offset  64: 29651.72
	offset  65: 29770.53
	offset  66: 29745.74
	offset  67: 29703.38
	offset  68: 29733.34
	offset  69: 29759.17
	offset  70: 29748.84
	offset  71: 29781.89
	offset  72: 29863.52
	offset  73: 29775.70
	offset  74: 29774.67
	offset  75: 29699.24
	offset  76: 29826.32
	offset  77: 29750.90
	offset  78: 29748.84
	offset  79: 29698.21
	offset  80: 29775.70
	offset  81: 29764.33
	offset  82: 29742.63
	offset  83: 29645.52
	offset  84: 29692.01
	offset  85: 29844.92
	offset  86: 29874.88
	offset  87: 29786.03
	offset  88: 29638.29
	offset  89: 29708.54
	offset  90: 29708.54
	offset  91: 29797.39
	offset  92: 29653.78
	offset  93: 29856.28
	offset  94: 29696.14
	offset  95: 29760.20
	offset  96: 29795.33
	offset  97: 29869.71
	offset  98: 29637.26
	offset  99: 29750.90
	offset 100: 29726.10
average		[min, max]	(range, stddev)
+ 29.766kHz		[29680, 29870]	(190, 47.825729)
overruns: 0
not found: 25499
average absolute error: -33.445 ppm
"""

class TestFn:
    def test_build_kal_scan_band_string_noargs(self):
        band = "GSM900"
        kal_bin = "/usr/bin/kal"
        control = "/usr/bin/kal -v -s GSM900"
        args = {}
        result = fn.build_kal_scan_band_string(kal_bin, band, args)
        assert result == control

    def test_build_kal_scan_band_string_args(self):
        band = "GSM900"
        kal_bin = "/usr/bin/kal"
        args = {"gain": 45}
        control = "/usr/bin/kal -v -s GSM900 -g 45"
        result = fn.build_kal_scan_band_string(kal_bin, band, args)
        assert result == control

    def test_herz_me(self):
        input_value = "99kHz"
        expected_output = 99000.0
        actual_output = fn.herz_me(input_value)
        assert actual_output == expected_output

    def test_determine_final_freq(self):
        base = 1
        direction = "+"
        modifier = 2
        assert fn.determine_final_freq(base, direction, modifier) == 3

    def test_to_eng(self):
        num_in = 5000000000000
        expected_num_out = "5E+12"
        actual_num_out = fn.to_eng(num_in)
        assert expected_num_out == actual_num_out

    def test_parse_kal_scan(self):
        control_channel = "231"
        control_base_freq = 889800000.0
        control_mod_freq = 22127.0
        control_modifier = "+"
        control_power = "348914.01"
        control_band = "GSM-850"
        control_gain = "45.0"
        control_sample_rate = "270833.002142"
        control_cdt = "261365.030729"
        control_device = "0: Generic RTL2832U OEM"
        kal_normalized = fn.parse_kal_scan(kal_scan_sample)
        assert kal_normalized[0]["channel"] == control_channel
        assert kal_normalized[0]["base_freq"] == control_base_freq
        assert kal_normalized[0]["mod_freq"] == control_mod_freq
        assert kal_normalized[0]["modifier"] == control_modifier
        assert kal_normalized[0]["power"] == control_power
        assert kal_normalized[0]["band"] == control_band
        assert kal_normalized[0]["gain"] == control_gain
        assert kal_normalized[0]["sample_rate"] == control_sample_rate
        assert kal_normalized[0]["channel_detect_threshold"] == control_cdt
        assert kal_normalized[0]["device"] == control_device

    def test_parse_channel_scan(self):
        control_offset = "29921.37"
        control_channel = "232"
        control_device = "0: Generic RTL2832U OEM"
        control_frequency = "890.0MHz"
        control_band = "GSM-850"
        control_iteration = "1"
        control_sample_rate = "270833.002142"
        control_gain = "45.0"
        kal_normalized = fn.parse_kal_channel(kal_freq_offset_sample)
        assert kal_normalized[0]["offset"] == control_offset
        assert kal_normalized[0]["channel"] == control_channel
        assert kal_normalized[0]["device"] == control_device
        assert kal_normalized[0]["iteration"] == control_iteration
        assert kal_normalized[0]["sample_rate"] == control_sample_rate
        assert kal_normalized[0]["gain"] == control_gain
        assert kal_normalized[0]["band"] == control_band
        assert kal_normalized[0]["frequency"] == control_frequency
