CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_search;


CREATE TABLE IF NOT EXISTS chunks (
    id        TEXT PRIMARY KEY,
    kaynak    TEXT,
    madde     TEXT,
    url       TEXT,
    metin     TEXT,
    embedding vector(1024)
);

CREATE INDEX IF NOT EXISTS chunks_bm25 ON chunks
USING paradedb (id, (metin::pdb.simple('stemmer=french', 'stopwords_language=French')));