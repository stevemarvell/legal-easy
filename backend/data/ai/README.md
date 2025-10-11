# AI-Generated Data Directory

This directory contains all AI-generated analysis, indexes, and derived data. This separation ensures clear distinction between source materials and AI-processed content.

## Directory Structure

```
ai/
├── research_corpus/
│   ├── research_corpus_index.json    # AI-generated corpus index
│   └── research_concepts.json        # AI-extracted legal concepts
└── case_documents/
    └── [AI analysis of case documents]
```

## Files

### research_corpus/
- **research_corpus_index.json**: AI-generated index of all research corpus materials with metadata, categorization, and relationships
- **research_concepts.json**: AI-extracted legal concepts, definitions, and relationships from corpus analysis

### case_documents/
- Contains AI-generated analysis of case documents (document summaries, key points extraction, etc.)

## Important Notes

- **Source Separation**: Original source materials remain in their respective directories (`/data/research_corpus/`, `/data/cases/`, etc.)
- **AI Processing**: All content in this directory is generated or processed by AI systems
- **Regeneration**: Files in this directory can be safely regenerated from source materials
- **Version Control**: Consider excluding large AI-generated files from version control and regenerating them as needed

## Related Services

- `DataService.regenerate_corpus_index()`: Regenerates the research corpus index
- `POST /api/corpus/regenerate-index`: API endpoint to trigger index regeneration
- Admin interface: Web UI for managing corpus index regeneration