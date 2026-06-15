-- SROS DuckDB Schema v0.1 (SXMU_MDD 驱动)
-- 用于 sros-db-server 的数据摄入目标
-- 来源: 03-Science_Projects/Project_SXMU_MDD_Twin/config/duckdb/schema.sql

-- 被试主表
CREATE TABLE IF NOT EXISTS subjects (
    subject_id VARCHAR PRIMARY KEY,
    cohort VARCHAR NOT NULL,              -- Adult_MDD, Adolescent_MDD, Adult_HC, Adolescent_HC
    age_group VARCHAR,                    -- adolescent (10-23), adult (24-55)
    sex VARCHAR,
    age_at_baseline FLOAT,
    group_status VARCHAR,                 -- MDD, HC, SR, FMT, dTMS
    intervention_type VARCHAR,            -- dTMS, FMT, SSRIs, IPT, none
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MRI 扫描记录
CREATE TABLE IF NOT EXISTS mri_scans (
    scan_id INTEGER PRIMARY KEY,
    subject_id VARCHAR REFERENCES subjects(subject_id),
    session_label VARCHAR,               -- baseline, week8, week12, month6, month8, month14
    modality VARCHAR,                     -- T1, BOLD, DTI, DICOM
    bids_path VARCHAR,                    -- BIDS 相对路径
    dicom_path VARCHAR,                   -- DICOM 原始路径
    scan_date DATE,
    file_size_gb FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 临床量表
CREATE TABLE IF NOT EXISTS clinical_scales (
    assessment_id INTEGER PRIMARY KEY,
    subject_id VARCHAR REFERENCES subjects(subject_id),
    session_label VARCHAR,
    scale_name VARCHAR,                   -- HAMD, HAMA, BSI-CV, CTQ, RBANS, etc.
    scale_score FLOAT,
    subscale_scores JSON,                 -- {"somatic": 12, "cognitive": 8, ...}
    assessment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EEG 记录
CREATE TABLE IF NOT EXISTS eeg_records (
    eeg_id INTEGER PRIMARY KEY,
    subject_id VARCHAR REFERENCES subjects(subject_id),
    session_label VARCHAR,
    paradigm VARCHAR,                     -- resting_EO, resting_EC, P300, P50, MMN, CNV
    channel_count INTEGER,                -- 64, 128
    file_path VARCHAR,
    file_size_gb FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 干预记录
CREATE TABLE IF NOT EXISTS interventions (
    intervention_id INTEGER PRIMARY KEY,
    subject_id VARCHAR REFERENCES subjects(subject_id),
    intervention_type VARCHAR,            -- dTMS, FMT, SSRIs, IPT
    start_date DATE,
    end_date DATE,
    parameters JSON,                      -- {"target": "left_DLPFC", "frequency": "10Hz", ...}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 宏基因组/多组学
CREATE TABLE IF NOT EXISTS omics_data (
    omics_id INTEGER PRIMARY KEY,
    subject_id VARCHAR REFERENCES subjects(subject_id),
    sample_type VARCHAR,                  -- stool, saliva, blood
    omics_type VARCHAR,                   -- metagenomics, metabolomics, qPCR, scRNA
    file_path VARCHAR,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 暴露体数据
CREATE TABLE IF NOT EXISTS exposome (
    exposome_id INTEGER PRIMARY KEY,
    subject_id VARCHAR REFERENCES subjects(subject_id),
    chemical_type VARCHAR,                -- PFAS, heavy_metal
    chemical_name VARCHAR,                -- PFOS, PFOA, Cd, Pb, etc.
    concentration FLOAT,
    unit VARCHAR,
    measurement_method VARCHAR,           -- HPLC-MS, ICP-MS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 脑网络特征 (计算产物)
CREATE TABLE IF NOT EXISTS brain_features (
    feature_id INTEGER PRIMARY KEY,
    subject_id VARCHAR REFERENCES subjects(subject_id),
    session_label VARCHAR,
    feature_type VARCHAR,                 -- functional_connectivity, structural_connectivity, graph_metric
    atlas VARCHAR,                        -- Schaefer2018, AAL, HCP_MMP
    feature_data_path VARCHAR,            -- .mat / .csv 文件路径
    derived_from JSON,                    -- 计算来源(script/commit hash)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_subjects_cohort ON subjects(cohort);
CREATE INDEX IF NOT EXISTS idx_subjects_group ON subjects(group_status);
CREATE INDEX IF NOT EXISTS idx_mri_subject ON mri_scans(subject_id);
CREATE INDEX IF NOT EXISTS idx_mri_modality ON mri_scans(modality);
CREATE INDEX IF NOT EXISTS idx_clinical_subject ON clinical_scales(subject_id);
CREATE INDEX IF NOT EXISTS idx_clinical_scale ON clinical_scales(scale_name);
CREATE INDEX IF NOT EXISTS idx_eeg_subject ON eeg_records(subject_id);
CREATE INDEX IF NOT EXISTS idx_intervention_subject ON interventions(subject_id);
CREATE INDEX IF NOT EXISTS idx_omics_subject ON omics_data(subject_id);
CREATE INDEX IF NOT EXISTS idx_exposome_subject ON exposome(subject_id);
CREATE INDEX IF NOT EXISTS idx_brain_features_subject ON brain_features(subject_id);
