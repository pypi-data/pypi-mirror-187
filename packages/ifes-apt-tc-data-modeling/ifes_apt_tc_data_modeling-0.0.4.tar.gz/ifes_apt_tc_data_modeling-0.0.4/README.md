# atomprobe-data-modeling

## Mission:
Foster exchange about data models and work towards specifications
of file formats from the research field of atom probe microscopy.

## Documentation of file formats and data models in atom probe status quo
In the field of atom probe microscopy detailed technical specification of the
file formats and data models in use is not available for all file formats.
A practical solution to address this limitation has been to collect instances,
i.e. example files in respective format, share and inspect them, so that
everybody can help and contribute to understand better what likely could be
the specification. Pieces of information about file formats are available
in the literature as in books by D. Larson et al. and B. Gault et al.
Individual members of the community like D. Haley have contributed much to
making the community aware of these limitations. Members like M. Kühbach
have driven the implementation and communication of the APT file format
introduced by AMETEK/Cameca with the APSuite software package.
Despite these efforts, this work is not complete.

Especially nowadays with an interest in aligning research and data stewardship
with the aims of the FAIR principles it became clear that it would be very
useful to exchange more details about data models and file formats as otherwise
it is not foreseeable how atom probe data can be made really interoperable
with electronic lab notebooks, research data management systems, and work with
tools other than of the proprietary formats of the technology partners.

In regards of this, understanding formats by examples, showed to be a slow and
error prone as the underlying source code which was used to write such files
and input, workflow, i.e. context in which the file and pieces of information
were created or numerically transformed (the provenance) might not have been
captured or/and the specific software tool(s) used might not be shared or 
publicly accessible openly.

## Benefit and Next Steps
You can easily imagine that the more people support us with this work that the
more complete our understanding and knowledge about the available file formats
in atom probe microscopy will become. This can help all of us in the long run to
build software tools which are more reliably and robustly capable of parsing
research data irrespective of which tools you use for digitalizing your
atom probe research.

The Python parsers in this repository are meant as one motivation to offer
immediate benefit to users, while the collection of examples and technical
discussions via issues serves the more long-term perspective aim to arrive
at a detailed specification or at least as robust as possible parser that
can work with all available file formats and translate between formats
and data models.

## Support us with this work
Thank you very much for supporting this activity and your time.

## Feedback, questions
Feel free to drop us a message via setting up or commenting on an issue
and feel free to use the resources in this repository.

## Where to place your examples?
There is a *examples_with_provenance* and *examples_without_provenance*
sub-directory for each file format.

When you do know with which software and measured dataset you have created a file,
you should share the file and these pieces of information (software version)
at least by naming the respective raw files. Ideally you share the examples via
offering a link to an external data repository such as Zenodo or other providers.
This not only avoids that this repository would get too much filled up with binary data.
Also it enables you to share clearly the under which license you make your examples
available.

## Provenance if possible, plain examples if in doubt
Use the *examples_with_provenance* sub-directory. With this it is at least possible
to reproduce the file creation. A practical solution is to share the screenshot to
achieve this is to upload a screenshot of the complete IVAS/APSuite version
info screen, i.e. including the APSuite version, the CernRoot version, the CamecaRoot
version, and the versions of libraries used by APSuite.

Atom probers should be aware that file formats like POS, ePOS, or APT are *not*
raw data nor are they specified. Instead, refer to RRAW, STR, RHIT and/or HITS files.
Ideally, you add unique identifiers (such as SHA256 checksums) for each raw file.
A documentation how you can do this was issued by your IFES APT TC colleagues.

When you cannot detail all these pieces of information you can still participate
and support us a lot if you share your knowledge by adding at least a link to a repository
or file share with content in the relevant atom-probe-specific file formats.
In this case, please use the *examples_without_provenance* directory.
While these examples are stripped of the context in which they were created
and used, these examples can still be very useful to run the file formats parsers
against and thus make these parsers more robust.

# Background information
Many file formats in the research field are not fully documented.
A checklist of the necessary pieces of information and documentation required
to call a data model, data schema, and/or file format fully documented in
accordance with the FAIR data and research software stewardship principles
is given below:

1. Each piece of information (bit/byte) is documented.
2. This documentation fulfills the FAIR principles, i.e.
   [Wilkinson et al., 2016](https://doi.org/10.1038/sdata.2016.18) and
   [Barker et al., 2022](https://doi.org/10.1038/s41597-022-01710-x)
   For binary files, tools like [kaitai struct](https://kaitai.io/) offer one strategy
   for describing the exact binary information content in the data
   item e.g. file, database entry, API post, but let alone this is insufficient.
3. To each piece of information there exists a parameterized description,
   what this piece of information means. One way to arrive at such description
   is to use a data schema or ontology.
   It is important to mention that the concepts in this schema/ontology have
   unique identifier so that each data item/piece of information is identifiable
   as an instance of an entry in a database or a knowledge graph.
   This holds independently of which research data management system
   or electronic lab notebook is used.
4. In addition, it is very useful that timestamps are associated with 
   each data item (ISO8061 with time zone information) so that it is possible
   to create a timeline of the context in which and when the e.g. file was created.

The first and second point is known as a specification with the additional
contextualization and specification offered by measures detailed in the FAIR principles.

