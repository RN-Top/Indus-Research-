<a name="ds-cldfmetadatajson"> </a>

# Wordlist CLDF Numeralbank Analysed

**CLDF Metadata**: [cldf-metadata.json](./cldf-metadata.json)

**Sources**: [sources.bib](./sources.bib)

property | value
 --- | ---
[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Bibiko, H.-H.; Koile, E.; Barlow, R.; Mamta, K.; Korobzow, N.; Appiah Tieku, E.; Rzymski, C.; List, J.-M.; Gray, R. D. (2025): Numeralbank. A Collection of Numeral Systems of the World's Languages. Leipzig: Max Planck Institute for Evolutionary Anthropology.
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF Wordlist](http://cldf.clld.org/v1.0/terms.rdf#Wordlist)
[dc:identifier](http://purl.org/dc/terms/identifier) | https://numerals.clld.org
[dc:license](http://purl.org/dc/terms/license) | https://creativecommons.org/licenses/by/4.0/
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://github.com/numeralbank/numeralbank-analysed
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/numeralbank/numeralbank-analysed/tree/03b11858">numeralbank/numeralbank-analysed  v0.9.1-124-g03b11858</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v5.3">Glottolog  v5.3</a></li><li><a href="https://github.com/concepticon/concepticon-data/tree/v3.4.0">Concepticon  v3.4.0</a></li><li><a href="https://github.com/cldf-clts/clts/tree/v2.3.0">CLTS  v2.3.0</a></li><li><a href="https://github.com/numeralbank/sand/tree/37683f0">numeralbank/sand  v1.0-1-g37683f0</a></li><li><a href="https://github.com/numeralbank/barlowpacific/tree/v1.8">numeralbank/barlowpacific  v1.8</a></li><li><a href="https://github.com/numeralbank/bowernnumerals/tree/a3e60bc">numeralbank/bowernnumerals  v0.8-1-ga3e60bc</a></li><li><a href="https://github.com/numeralbank/googleuninum/tree/b9ece9f">numeralbank/googleuninum  b9ece9f</a></li><li><a href="https://github.com/numeralbank/numerals/tree/1ff39840">numeralbank/numerals  1ff39840</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>lingpy-rcParams</strong>: <a href="./lingpy-rcParams.json">lingpy-rcParams.json</a></li><li><strong>python</strong>: 3.10.20</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | numeralbank-analysed
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-formscsv"></a>Table [forms.csv](./forms.csv)

CustomLexeme(ID: str, Form: str, Value: str, Language_ID: str, Parameter_ID: str, Local_ID: Optional[str] = None, Segments: list[str] = <factory>, Graphemes: Optional[list[str]] = None, Profile: Optional[str] = None, Source: list[str] = <factory>, Comment: Optional[str] = None, Cognacy: Optional[str] = None, Loan: Optional[bool] = None, NumberValue: int | None = None, Gloss: str | None = None, GlossClean: str | None = None, GlossMath: str | None = None, GlossCalc: str | None = None)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF FormTable](http://cldf.clld.org/v1.0/terms.rdf#FormTable)
[dc:extent](http://purl.org/dc/terms/extent) | 265928


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Local_ID](http://purl.org/dc/terms/identifier) | `string` | 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [parameters.csv::ID](#table-parameterscsv)
[Value](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 
[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | 
[Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | 
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Cognacy` | `string` | 
`Loan` | `boolean` | 
`Graphemes` | `string` | 
`Profile` | `string` | 
`NumberValue` | `string` | 
`Gloss` | `string` | 
`GlossClean` | `string` | 
`GlossMath` | `string` | 
`GlossCalc` | `string` | 

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

CustomLanguage(ID: str = '', Name: Optional[str] = None, ISO639P3code: Optional[str] = None, Glottocode: Optional[str] = None, Macroarea: Optional[str] = None, Latitude: Optional[float] = None, Longitude: Optional[float] = None, Glottolog_Name: Optional[str] = None, Family: Optional[str] = None, Dataset: str | None = None, BaseAnnotation: str | None = None, BaseAnnotator: str | None = None, BaseComment: str | None = None, Coverage: float | None = None, OneToThirty: float | None = None, BaseInSource: str | None = None)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 9120


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | 
`Glottolog_Name` | `string` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal`<br>&ge; -90<br>&le; 90 | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal`<br>&ge; -180<br>&le; 180 | 
`Family` | `string` | 
`Dataset` | `string` | 
`BaseAnnotation` | `string` | 
`BaseAnnotator` | `string` | 
`BaseComment` | `string` | 
`Coverage` | `float` | Coverage of the language in comparison with our master concept list.
`OneToThirty` | `string` | 
`BaseInSource` | `string` | 

## <a name="table-parameterscsv"></a>Table [parameters.csv](./parameters.csv)

Essential data of a concept mapped to Concepticon.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 168


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Concepticon_ID](http://cldf.clld.org/v1.0/terms.rdf#concepticonReference) | `string` | 
`Concepticon_Gloss` | `string` | 

## <a name="table-contributionscsv"></a>Table [contributions.csv](./contributions.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ContributionTable](http://cldf.clld.org/v1.0/terms.rdf#ContributionTable)
[dc:extent](http://purl.org/dc/terms/extent) | 5


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Citation](http://cldf.clld.org/v1.0/terms.rdf#citation) | `string` | 
`Metadata` | `string` | JSON encoded metadata of used datasets
