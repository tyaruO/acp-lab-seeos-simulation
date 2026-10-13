from __future__ import annotations

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
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
