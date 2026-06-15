#!/bin/bash
#SBATCH --job-name=graphmri_sub-{SUBJECT}
#SBATCH --output=logs/graphmri_sub-{SUBJECT}_%j.out
#SBATCH --error=logs/graphmri_sub-{SUBJECT}_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --partition=cpu

# SROS — 脑网络矩阵提取模板 (GraphMRI / 自定义)
# 使用方法: sed 's/{SUBJECT}/sub-001/g' config/slurm/graphmri_template.slurm > job.slurm && sbatch job.slurm
# 或通过 sros-hpc-server 自动替换

set -e

SUBJECT={SUBJECT}
DERIV_DIR={DERIV_DIR}
OUTPUT_DIR={OUTPUT_DIR}/graphmri
SCRIPT_DIR={SCRIPT_DIR}

mkdir -p "$OUTPUT_DIR/$SUBJECT" logs

module load python/3.11

python "$SCRIPT_DIR/extract_brain_graph.py" \
    --fmriprep_dir "$DERIV_DIR/fmriprep/$SUBJECT" \
    --qsiprep_dir "$DERIV_DIR/qsiprep/$SUBJECT" \
    --output_dir "$OUTPUT_DIR/$SUBJECT" \
    --atlas Schaefer2018_400Parcels_7Networks \
    --metrics degree centrality clustering efficiency
