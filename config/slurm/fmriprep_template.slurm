#!/bin/bash
#SBATCH --job-name=fmriprep_sub-{SUBJECT}
#SBATCH --output=logs/fmriprep_sub-{SUBJECT}_%j.out
#SBATCH --error=logs/fmriprep_sub-{SUBJECT}_%j.err
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --partition=cpu

# SROS — fMRIPrep 预处理模板
# 使用方法: sed 's/{SUBJECT}/sub-001/g' config/slurm/fmriprep_template.slurm > job.slurm && sbatch job.slurm
# 或通过 sros-hpc-server 自动替换

set -e

SUBJECT={SUBJECT}
BIDS_DIR={BIDS_DIR}
OUTPUT_DIR={OUTPUT_DIR}
WORK_DIR={WORK_DIR}/fmriprep_${SUBJECT}
CONTAINER={CONTAINER_PATH}
FS_LICENSE={FS_LICENSE_PATH}

mkdir -p "$OUTPUT_DIR" "$WORK_DIR" logs

module load apptainer

apptainer run \
    --bind /lustre:/lustre \
    --cleanenv \
    "$CONTAINER" \
    "$BIDS_DIR" "$OUTPUT_DIR" participant \
    --participant-label "$SUBJECT" \
    --fs-license-file "$FS_LICENSE" \
    --work-dir "$WORK_DIR" \
    --nthreads 8 \
    --mem-mb 32000 \
    --output-spaces MNI152NLin2009cAsym:res-2 \
    --skip-bids-validation
