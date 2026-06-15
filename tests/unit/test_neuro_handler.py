"""Unit tests for NeuroHandler: BIDS validation + graphmri script generation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sros.servers.neuro.handler import NeuroHandler, GRAPHMRI_DEFAULT_CONFIG


class TestBIDSValidation:
    """BIDS structural validation tests."""

    def test_validate_bids_missing_dir(self, tmp_path: Path) -> None:
        """Non-existent directory returns error."""
        handler = NeuroHandler()
        result = handler.validate_bids(str(tmp_path / "nonexistent"))
        assert result["ok"] is False
        assert "not found" in result["error"]

    def test_validate_bids_empty_dir(self, tmp_path: Path) -> None:
        """Empty directory is valid but has zero subjects."""
        result = NeuroHandler().validate_bids(str(tmp_path))
        assert result["ok"] is True
        assert result["subject_count"] == 0
        assert result["nifti_count"] == 0

    def test_validate_bids_minimal_subject(self, tmp_path: Path) -> None:
        """Minimal BIDS structure with one subject, one session, one modality."""
        sub_dir = tmp_path / "sub-001" / "ses-01" / "anat"
        sub_dir.mkdir(parents=True)
        (sub_dir / "sub-001_ses-01_T1w.nii.gz").write_text("mock")

        result = NeuroHandler().validate_bids(str(tmp_path))
        assert result["ok"] is True
        assert result["subject_count"] == 1
        assert result["session_count"] == 1
        assert "anat" in result["modalities"]
        assert result["nifti_count"] == 1
        assert result["valid"] is True

    def test_validate_bids_multiple_subjects(self, tmp_path: Path) -> None:
        """Multiple subjects across different modalities."""
        for sid in ["sub-001", "sub-002", "sub-003"]:
            for ses in ["ses-01"]:
                for mod in ["anat", "func"]:
                    mod_dir = tmp_path / sid / ses / mod
                    mod_dir.mkdir(parents=True)
                    (mod_dir / f"{sid}_{ses}_desc.nii.gz").write_text("mock")

        result = NeuroHandler().validate_bids(str(tmp_path))
        assert result["subject_count"] == 3
        assert result["nifti_count"] == 6
        assert "anat" in result["modalities"]
        assert "func" in result["modalities"]

    def test_validate_bids_invalid_subject_name(self, tmp_path: Path) -> None:
        """Invalid subject directory name (matches sub-* glob but fails regex) flagged as error."""
        (tmp_path / "sub-bad@name").mkdir()
        result = NeuroHandler().validate_bids(str(tmp_path))
        issues = result["issues"]
        assert any(i["level"] == "error" for i in issues)
        assert result["valid"] is False

    def test_validate_bids_dataset_description_warning(self, tmp_path: Path) -> None:
        """Missing dataset_description.json issues a warning."""
        result = NeuroHandler().validate_bids(str(tmp_path))
        assert any(i["file"] == "dataset_description.json" for i in result["issues"])

    def test_validate_bids_no_validator_by_default(self, tmp_path: Path) -> None:
        """bids-validator is not run unless explicitly requested."""
        result = NeuroHandler().validate_bids(str(tmp_path))
        assert result["bids_validator"] is None


class TestGraphMRIGeneration:
    """graphmri script generation tests."""

    def test_generate_graphmri_basic(self, tmp_path: Path) -> None:
        """Generate a basic graphmri script with defaults."""
        bids_dir = tmp_path / "bids"
        bids_dir.mkdir()
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = NeuroHandler().generate_graphmri_script(
            subject_id="sub-001",
            bids_dir=str(bids_dir),
            output_dir=str(output_dir),
        )
        assert result["ok"] is True
        script_path = Path(result["script_path"])
        assert script_path.exists()
        assert script_path.name == "graphmri_sub-001.py"

        content = script_path.read_text()
        assert "sub-001" in content
        assert "graphmri" in content.lower()

    def test_generate_graphmri_custom_config(self, tmp_path: Path) -> None:
        """Custom config overrides graphmri defaults."""
        bids_dir = tmp_path / "bids"
        bids_dir.mkdir()
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = NeuroHandler().generate_graphmri_script(
            subject_id="sub-002",
            bids_dir=str(bids_dir),
            output_dir=str(output_dir),
            config={"atlas": "desikan", "parcellation": 68},
            connectivity_matrices=["fisher_z", "partial"],
        )
        assert result["ok"] is True
        content = Path(result["script_path"]).read_text()
        assert "desikan" in content
        assert "68" in content
        assert "fisher_z" in content

    def test_generate_graphmri_creates_output_dir(self, tmp_path: Path) -> None:
        """Output directory is created if it doesn't exist."""
        bids_dir = tmp_path / "bids"
        bids_dir.mkdir()

        result = NeuroHandler().generate_graphmri_script(
            subject_id="sub-003",
            bids_dir=str(bids_dir),
            output_dir=str(tmp_path / "new_output"),
        )
        assert result["ok"] is True
        assert Path(result["script_path"]).exists()

    def test_generate_graphmri_default_config_structure(self) -> None:
        """Default config has required keys."""
        assert "atlas" in GRAPHMRI_DEFAULT_CONFIG
        assert "parcellation" in GRAPHMRI_DEFAULT_CONFIG
        assert "edge_weights" in GRAPHMRI_DEFAULT_CONFIG
        assert len(GRAPHMRI_DEFAULT_CONFIG["edge_weights"]) >= 2


class TestFMRIPrepBatch:
    """fMRIPrep batch generation tests."""

    def test_generate_fmriprep_batch(self, tmp_path: Path) -> None:
        """Generate fMRIPrep scripts for multiple subjects."""
        bids_dir = tmp_path / "bids"
        bids_dir.mkdir()
        output_dir = tmp_path / "jobs"
        output_dir.mkdir()

        result = NeuroHandler().generate_fmriprep_batch(
            subject_ids=["sub-001", "sub-002"],
            bids_dir=str(bids_dir),
            output_dir=str(output_dir),
        )
        assert result["ok"] is True
        assert result["count"] == 2
        assert len(result["scripts"]) == 2
        for sp in result["scripts"]:
            assert Path(sp).exists()
            content = Path(sp).read_text()
            assert "#SBATCH" in content, f"Not a valid Slurm script: {sp}"

    def test_generate_fmriprep_batch_missing_template(self, tmp_path: Path) -> None:
        """Custom template that doesn't exist returns error."""
        result = NeuroHandler().generate_fmriprep_batch(
            subject_ids=["sub-001"],
            bids_dir=str(tmp_path),
            output_dir=str(tmp_path),
            template="/nonexistent/template.slurm",
        )
        assert result["ok"] is False
        assert "not found" in result["error"]

    def test_generate_fmriprep_batch_empty_subjects(self, tmp_path: Path) -> None:
        """Empty subject list returns 0 scripts."""
        bids_dir = tmp_path / "bids"
        bids_dir.mkdir()
        output_dir = tmp_path / "jobs"
        output_dir.mkdir()

        result = NeuroHandler().generate_fmriprep_batch(
            subject_ids=[],
            bids_dir=str(bids_dir),
            output_dir=str(output_dir),
        )
        assert result["ok"] is True
        assert result["count"] == 0
