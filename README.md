# Start here

Bare-bones models for genomics and bioinformatics data types.

It's also a way to start decoupling the complex logic of DAta NEtwork, bioinformatics-tools, and BSP into proper microservices and python libraries. For instance, a lot of logic for bioinformatics can be reused, with the technical implementation/deployment differing.

## Services

- simple modeling of bioinformatics files
  - should this include validation?
  - Pydantic models
- Database integration
  - SQLAlchemy
  - If there needs to be a Pydatic -> SQLAlchemy adapter, should 
- parsing of bioinformatics/other files
  - should this take care of chunking per-entry and then feed into modeler?
  - weigh, justify, and document the pros and cons of chunking per-entry and per file and how to relate
- caragols for command line parsing
- api(s)?
- GUIs