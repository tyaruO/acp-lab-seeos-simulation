from acp_lab.signal_analysis import summarize_waveform


def test_summary_basic():
    result = summarize_waveform([1, -1, 1, -1], sample_rate_hz=2)

    assert result["sample_count"] == 4
    assert result["duration_s"] == 2.0
    assert result["peak_abs_amplitude"] == 1.0
    assert result["rms_amplitude"] == 1.0


def test_warning_flag():
    result = summarize_waveform([0.5, 0.4, 0.3], sample_rate_hz=3, warning_peak=0.45)
    assert result["threshold_warning"] is True


def test_invalid_rate():
    try:
        summarize_waveform([1, 2], sample_rate_hz=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for non-positive sample rate")
