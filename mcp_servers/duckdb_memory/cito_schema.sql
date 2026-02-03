-- CiTO (Citation Typing Ontology) Schema for DuckDB

-- Papers table
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    venue TEXT,
    doi TEXT UNIQUE,
    abstract TEXT,
    citation_key TEXT UNIQUE
);

-- Citations table (paper A cites paper B)
CREATE TABLE IF NOT EXISTS citations (
    id INTEGER PRIMARY KEY,
    citing_paper_id INTEGER REFERENCES papers(id),
    cited_paper_id INTEGER REFERENCES papers(id),
    citation_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relationships table (CiTO relationships between papers)
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    subject_paper_id INTEGER REFERENCES papers(id),
    object_paper_id INTEGER REFERENCES papers(id),
    relationship_type TEXT NOT NULL, -- e.g., 'critiques', 'extends', 'usesMethodFrom'
    confidence_score REAL,
    evidence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Research gaps table
CREATE TABLE IF NOT EXISTS research_gaps (
    id INTEGER PRIMARY KEY,
    manuscript_section TEXT,
    gap_description TEXT,
    priority INTEGER,
    status TEXT DEFAULT 'open', -- 'open', 'researched', 'addressed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi);
CREATE INDEX IF NOT EXISTS idx_papers_citation_key ON papers(citation_key);
CREATE INDEX IF NOT EXISTS idx_citations_citing ON citations(citing_paper_id);
CREATE INDEX IF NOT EXISTS idx_citations_cited ON citations(cited_paper_id);
CREATE INDEX IF NOT EXISTS idx_relationships_subject ON relationships(subject_paper_id);
CREATE INDEX IF NOT EXISTS idx_relationships_object ON relationships(object_paper_id);
CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relationship_type);