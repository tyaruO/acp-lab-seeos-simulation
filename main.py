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
