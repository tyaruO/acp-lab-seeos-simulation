# ACP-Lab — acoustic experiment software scaffold

This repository contains a small Python scaffold for logging and summarizing acoustic experiment data.

It is an early research-oriented software scaffold intended for lab data capture and waveform summaries. It is not a medical device, does not establish biological efficacy, and does not certify acoustic or clinical safety.

## Scope

- Record experimental settings and measurements as JSON.
- Summarize a supplied waveform (RMS, peak amplitude, duration).
- Flag values exceeding a user-configured threshold for review.
- Keep the safety and validation logic explicit: thresholds are review flags only, not safety limits.

## Repository layout

```text
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
```

## Requirements

- Python 3.10+
- NumPy
- pytest (for running the included tests)

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run the demo

```bash
python main.py
```

This creates an example `example_run.json` file in the repository root using synthetic data.

## Example output

```python
{
  "run": {
    "run_id": "demo-001",
    "sample_rate_hz": 20000.0,
    "transducer_frequency_hz": 1000000.0,
    "drive_voltage_v": 1.0,
    "medium": "synthetic demo signal",
    "notes": "Synthetic data only; not a real acoustic measurement.",
    "created_at_utc": "2026-01-01T12:00:00+00:00"
  },
  "measurements": {
    "sample_count": 1000,
    "sample_rate_hz": 20000.0,
    "duration_s": 0.05,
    "peak_abs_amplitude": 0.7,
    "rms_amplitude": 0.495,
    "mean_amplitude": 0.0,
    "threshold_warning": false,
    "threshold_note": "User-configured review threshold only; not a medical or acoustic safety limit."
  }
}
```

## Notes

- Threshold values are user-defined and are intended for review workflows only.
- They should not be interpreted as medical, safety, or engineering limits without appropriate calibration and validation in the target application.
- The project is intentionally small and transparent to serve as a starter scaffold for experiment logging and waveform review.
