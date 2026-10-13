from __future__ import annotations

import numpy as np


def summarize_waveform(samples, sample_rate_hz: float, warning_peak: float | None = None):
    """Summarize a waveform. Any threshold is user-defined and is not a safety limit."""
    x = np.asarray(samples, dtype=float)

    if x.ndim != 1 or x.size == 0:
        raise ValueError("samples must be a non-empty 1D sequence")

    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")

    if not np.all(np.isfinite(x)):
        raise ValueError("samples must contain only finite values")

    peak = float(np.max(np.abs(x)))

    result = {
        "sample_count": int(x.size),
        "sample_rate_hz": float(sample_rate_hz),
        "duration_s": float(x.size / sample_rate_hz),
        "peak_abs_amplitude": peak,
        "rms_amplitude": float(np.sqrt(np.mean(np.square(x)))),
        "mean_amplitude": float(np.mean(x)),
        "threshold_warning": bool(warning_peak is not None and peak > warning_peak),
        "threshold_note": (
            "User-configured review threshold only; "
            "not a medical or acoustic safety limit."
        ),
    }

    return result
