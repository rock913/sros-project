-- CiTO (Citation Typing Ontology) Schema for DuckDB

-- Sequences for IDs
CREATE SEQUENCE IF NOT EXISTS seq_papers_id;
CREATE SEQUENCE IF NOT EXISTS seq_citations_id;
CREATE SEQUENCE IF NOT EXISTS seq_relationships_id;
CREATE SEQUENCE IF NOT EXISTS seq_research_gaps_id;

-- Papers table
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_papers_id'),
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    venue TEXT,
    doi TEXT,
    abstract TEXT,
    citation_key TEXT
);

-- Citations table (paper A cites paper B)
CREATE TABLE IF NOT EXISTS citations (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_citations_id'),
    citing_paper_id INTEGER REFERENCES papers(id),
    cited_paper_id INTEGER REFERENCES papers(id),
    citation_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relationships table (CiTO relationships between papers)
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_relationships_id'),
    subject_paper_id INTEGER REFERENCES papers(id),
    object_paper_id INTEGER REFERENCES papers(id),
    relationship_type TEXT NOT NULL, -- e.g., 'critiques', 'extends', 'usesMethodFrom'
    confidence_score REAL,
    evidence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Research gaps table
CREATE TABLE IF NOT EXISTS research_gaps (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_research_gaps_id'),
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
