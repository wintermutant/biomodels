# Start here

Bare-bones models for genomics and bioinformatics data types.

It's also a way to start decoupling the complex logic of DAta NEtwork, bioinformatics-tools, and BSP into proper microservices and python libraries. For instance, a lot of logic for bioinformatics can be reused, with the technical implementation/deployment differing.

- have a .env file with BIOMODELS_DB_CONNECTION set and then source it

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


## biomodels
For this, this is only database models. The logic to extend the functionality of what you can actually
do with a specific file type should be reserved for biotools. Thus:
- biomodels will be a bioinformatics-specific ORM service that sets up all the modeling for you
- biotools builds functional data classes on top of common biomodels
  - this includes meta-stats
  - In this way, biotools does not necessarily need the ORM functionality of biomodels --> only if we want to store data
- if we want to retrieve data from a database and then run functionality, we'll need biomodels and biotools
  - if we just have the data in memory, we can use biotools
- biocompute will be the service that connects to SLURM (BSP)
- bioserver will be the API service that uses biomodels and biotools to do all the functionality
- biogui will be a GUI built on top of the API
- caragols will be the connectivity to CLI and configuration

## architectural notes
- biotools should rely on caragols, which is the report generator, config management, and CLI extender
  - Caragols also registers all of the do_ functionality and reports it in help to the CLI