# acp-lab-seeos-simulation
ACP-Lab/
├── README.md
├── requirements.txt
├── main.py
├── acp_lab/
│   ├── __init__.py
│   ├── models.py
│   └── signal_analysis.py
└── tests/
    └── test_signal_analysis.py

    # ACP-Lab — acoustic experiment software scaffold

This is an early software scaffold for logging and summarizing acoustic experiments.
It is **not** a medical device, does not establish biological efficacy, and does not certify acoustic or clinical safety.

## Scope
- Record experimental settings and measurements as JSON.
- Summarize a supplied waveform (RMS, peak amplitude, duration).
- Flag values that exceed user-configured thresholds for review.

## Run
Requires Python 3.10+ and NumPy.

```bash
python -m pip install -r requirements.txt
python main.py



## 2. `requirements.txt`

```text
numpy>=1.24


import numpy as np
from acp_lab.models import AcousticRun
from acp_lab.signal_analysis import summarize_waveform


def main():
    # Synthetic example only; replace with properly calibrated instrument data.
    sample_rate = 20_000
    t = np.arange(0, 0.05, 1 / sample_rate)
    waveform = 0.7 * np.sin(2 * np.pi * 1_000 * t)

    run = AcousticRun(
        run_id="demo-001",
        sample_rate_hz=sample_rate,
        transducer_frequency_hz=1_000_000,
        drive_voltage_v=1.0,
        medium="synthetic demo signal",
        notes="Synthetic data only; not a real acoustic measurement.",
    )
    summary = summarize_waveform(waveform, sample_rate, warning_peak=0.8)
    run.to_json("example_run.json", summary)
    print("Wrote example_run.json")
    print(summary)


if __name__ == "__main__":
    main()



"""ACP-Lab experimental data and signal-analysis scaffold."""


from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


@dataclass
class AcousticRun:
    run_id: str
    sample_rate_hz: float
    transducer_frequency_hz: float
    drive_voltage_v: float
    medium: str
    notes: str = ""
    created_at_utc: str = ""

    def validate(self) -> None:
        if not self.run_id.strip():
            raise ValueError("run_id must not be empty")
        if self.sample_rate_hz <= 0:
            raise ValueError("sample_rate_hz must be positive")
        if self.transducer_frequency_hz <= 0:
            raise ValueError("transducer_frequency_hz must be positive")
        if self.drive_voltage_v < 0:
            raise ValueError("drive_voltage_v must not be negative")
        if not self.medium.strip():
            raise ValueError("medium must not be empty")
        if not self.created_at_utc:
            self.created_at_utc = datetime.now(timezone.utc).isoformat()

    def to_json(self, path: str | Path, measurements: dict[str, Any]) -> None:
        self.validate()
        payload = {"run": asdict(self), "measurements": measurements}
        Path(path).write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8"
        )


import numpy as np


def summarize_waveform(
    samples,
    sample_rate_hz: float,
    warning_peak: float | None = None
):
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
        "threshold_warning": bool(
            warning_peak is not None and peak > warning_peak
        ),
        "threshold_note": (
            "User-configured review threshold only; "
            "not a medical or acoustic safety limit."
        ),
    }

    return result



import pytest
from acp_lab.signal_analysis import summarize_waveform


def test_summary_basic():
    result = summarize_waveform(
        [1, -1, 1, -1],
        sample_rate_hz=2
    )

    assert result["sample_count"] == 4
    assert result["duration_s"] == 2.0
    assert result["peak_abs_amplitude"] == 1.0
    assert result["rms_amplitude"] == 1.0


def test_invalid_rate():
    with pytest.raises(ValueError):
        summarize_waveform([1, 2], sample_rate_hz=0)


