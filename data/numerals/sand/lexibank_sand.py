from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomConcept(pylexibank.Concept):
    Number = attr.ib(default=None)
    NumberValue = attr.ib(default=None)


@attr.s
class CustomLanguage(pylexibank.Language):
    Family = attr.ib(default=None)
    Comment = attr.ib(default=None)
    Base = attr.ib(default=None)
    Sources = attr.ib(default=None)


@attr.s
class CustomLexeme(pylexibank.Lexeme):
    NumeralAnalysis = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "sand"
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    form_spec = pylexibank.FormSpec(replacements=[(" ", "_"), ("\u034f", ""),
                                                  (" ̌c"[1:], "č")])

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        concepts = {}
        language_errors = set()
        concept_errors = set()

        for concept in self.concepts:
            idx = concept["ID"] + "_" + slug(concept["ENGLISH"])
            args.writer.add_concept(
                ID=idx,
                Name=concept["ENGLISH"].lower(),
                Number=concept["ID"],
                Concepticon_ID=concept["CONCEPTICON_ID"],
                Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
            )
            concepts[concept["ENGLISH"].lower()] = idx

        languages = args.writer.add_languages(lookup_factory="ID")
        source_map = {r['ID']: r['Sources'] for r in self.etc_dir.read_csv('languages.tsv', dicts=True, delimiter='\t')}

        for row in self.raw_dir.read_csv("cardinals.tsv", dicts=True, delimiter="\t"):
            if row["Concept"] and row["Value"]:
                if row["Language"] not in languages:
                    language_errors.add(("language", row["Language"]))
                elif row["Concept"].lower() not in concepts:
                    concept_errors.add(("concept", row["Concept"]))
                else:
                    args.writer.add_forms_from_value(
                        Language_ID=languages[row["Language"]],
                        Parameter_ID=concepts[row["Concept"].lower()],
                        Value=row["Value"],
                        Source=source_map.get(row["Language"], ""),
                    )

        print("LANGUAGE ERRORS: ------------")
        for k, v in language_errors:
            print(k, v)

        print("CONCEPT ERRORS: ------------")
        for k, v in concept_errors:
            print(k, v)
