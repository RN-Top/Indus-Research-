import json
import pathlib
import shutil
import subprocess
from collections import ChainMap, Counter, defaultdict, namedtuple
from dataclasses import dataclass, field

import pycldf
from cldfzenodo.api import API as ZenodoAPI
from cldfzenodo.record import GithubRepos
from clldutils.misc import slug
from git import Repo, GitCommandError
from pylexibank import Dataset as BaseDataset, Language, Lexeme
from unidecode import unidecode


# just to save me some typing
CLDF_ID = 'http://cldf.clld.org/v1.0/terms.rdf#id'
CLDF_NAME = 'http://cldf.clld.org/v1.0/terms.rdf#name'
CLDF_GLOTTOCODE = 'http://cldf.clld.org/v1.0/terms.rdf#glottocode'
CLDF_FORM = 'http://cldf.clld.org/v1.0/terms.rdf#form'
CLDF_VALUE = 'http://cldf.clld.org/v1.0/terms.rdf#value'
CLDF_COMMENT = 'http://cldf.clld.org/v1.0/terms.rdf#comment'
CLDF_LATITUDE = 'http://cldf.clld.org/v1.0/terms.rdf#latitude'
CLDF_LONGITUDE = 'http://cldf.clld.org/v1.0/terms.rdf#longitude'
CLDF_MACROAREA = 'http://cldf.clld.org/v1.0/terms.rdf#macroarea'
CLDF_LANGUAGE_ID = 'http://cldf.clld.org/v1.0/terms.rdf#languageReference'
CLDF_PARAMETER_ID = 'http://cldf.clld.org/v1.0/terms.rdf#parameterReference'
CLDF_CONCEPTICON_ID = 'http://cldf.clld.org/v1.0/terms.rdf#concepticonReference'

GlossKey = namedtuple('GlossKey', 'language_id parameter_id value')

def collect_glosses(csv_rows):
    return {
        GlossKey(
            language_id=row['Language_ID'],
            parameter_id=row['Parameter_ID'],
            value=row['Value']):
        row
        for row in csv_rows}


def simple_chars(chars):
    return slug(unidecode(chars).replace('@', 'a'))


@dataclass
class CustomLexeme(Lexeme):
    NumberValue: int | None = None
    Gloss: str | None = None
    GlossClean: str | None = None
    GlossMath: str | None = None
    GlossCalc: str | None = None
    AlternateGloss: str | None = None
    CommentGlosser: str | None = None


@dataclass
class CustomLanguage(Language):
    Dataset: str | None = None
    BaseAnnotation: str | None = None
    BaseAnnotator: str | None = None
    BaseComment: str | None = None
    Coverage: float | None = field(
        default=None,
        metadata={
            'datatype': 'float',
            'dc:description': 'Coverage of the language in comparison with our master concept list.',
        })
    OneToThirty: float | None = None
    BaseInSource: str | None = None


def coverage(forms, concept_set):
    language_concepts = {
        (form[CLDF_LANGUAGE_ID], form['Concepticon_Gloss'])
        for form in forms
        if form['Concepticon_Gloss'] in concept_set}
    counts = Counter(
        language_id
        for language_id, _ in language_concepts)
    return {
        language_id: count / len(concept_set)
        for language_id, count in counts.most_common()}


class GitError(Exception):
    pass


def git_last_commit_date(path, git_command=None):
    if git_command is None:
        git_command = shutil.which('git')
    path = pathlib.Path(path)
    if not path.exists():
        raise GitError('cannot read from non-existent directory')
    path = path.resolve()
    cmd = [
        git_command,
        '--git-dir={}'.format(path / '.git'),
        '--no-pager',
        'log',
        '-1',
        '--format="%ai"',
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
            res = stdout.strip()  # pragma: no cover
        else:
            # throwing a custom error so it doesn't get caught by the local
            # except block
            raise GitError(stderr)
    except (ValueError, FileNotFoundError):
        return ''
    if not isinstance(res, str):
        res = res.decode('utf8')
    return res.replace('"', '')


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = 'numeralbank-analysed'
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    def cmd_download(self, args):
        self.dataset_meta = {
            r['ID']: r['URL']
            for r in self.etc_dir.read_csv('datasets.tsv', delimiter='\t', dicts=True)
        }

        github_info = {
            rec.doi: rec.github_repos
            for rec in ZenodoAPI.iter_records(community='lexibank', allversions=True)}

        for dataset, src in self.dataset_meta.items():
            ghinfo = github_info[src] if src in github_info else GithubRepos.from_url(src)
            args.log.info('Checking %s', dataset)
            dest = self.raw_dir / dataset

            # download data
            if dest.exists():
                args.log.info('... dataset already exists, pulling changes')
                for remote in Repo(str(dest)).remotes:
                    remote.fetch()
            else:
                args.log.info('... cloning %s', dataset)
                try:
                    Repo.clone_from(ghinfo.clone_url, str(dest))
                except GitCommandError as e:
                    args.log.error('... download failed\n %s', str(e))
                    continue

            # check out release (fall back to master branch)
            repo = Repo(str(dest))
            if ghinfo.tag:
                args.log.info('... checking out tag %s', ghinfo.tag)
                repo.git.checkout(ghinfo.tag)
            else:
                args.log.warning('... could not determine tag to check out')
                args.log.info('... checking out master')
                try:
                    branch = repo.branches.main
                    branch.checkout()
                except AttributeError:
                    try:
                        branch = repo.branches.master
                        branch.checkout()
                    except AttributeError:
                        args.log.error('found neither main nor master branch')
                repo.git.merge()

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        concepts = {
            concept['CONCEPTICON_GLOSS']: concept for concept in self.concepts}
        datasets = {
            r['ID']: (r['Source'], r['URL'])
            for r in self.etc_dir.read_csv('datasets.tsv', delimiter='\t', dicts=True)
        }

        args.writer.cldf.add_component(
            'ContributionTable',
            {
                'datatype': 'string',
                'name': 'Metadata',
                'dc:description': 'JSON encoded metadata of used datasets',
            },
        )
        for c in ['Description', 'Contributor']:
            args.writer.cldf.remove_columns('ContributionTable', c)

        for ds, (src, url) in datasets.items():
            cldf_path = self.raw_dir / ds / 'cldf' / 'cldf-metadata.json'
            with open(cldf_path) as f:
                js = json.load(f)
            doi = None
            git_version = None
            if 'github.com' in url.lower():
                access_url = url
                git_version = git_last_commit_date(cldf_path.parent.parent)
            else:
                doi = url
                access_url = f'https://doi.org/{doi}'

            args.writer.objects['contributions.csv'].append(
                {
                    'ID': js['rdf:ID'],
                    'Name': js['dc:title'],
                    'Citation': js['dc:bibliographicCitation'],
                    'Metadata': json.dumps(
                        {
                            'dcat:accessURL': access_url,
                            'dc:description': js.get('dc:description', None),
                            'dc:license': js.get('dc:license', None),
                            'aboutUrl': js.get('aboutUrl', None),
                            'doi': doi,
                            'git_version': git_version,
                            'source': src,
                        },
                    ),
                },
            )

        cldf_datasets = [
            pycldf.Dataset.from_metadata(self.raw_dir / ds / 'cldf' / 'cldf-metadata.json')
            for ds in datasets]

        languages = {}
        forms = []

        for ds in cldf_datasets:
            dsid = ds.metadata_dict['rdf:ID']
            args.log.info('Loading data from %s', dsid)
            ds_languages = {
                lg[CLDF_ID]: lg
                for lg in ds.iter_rows(
                    'LanguageTable',
                    CLDF_ID,
                    CLDF_NAME,
                    CLDF_GLOTTOCODE,
                    CLDF_LATITUDE,
                    CLDF_LONGITUDE,
                    CLDF_MACROAREA)}
            for lg in ds_languages.values():
                lg[CLDF_ID] = f'{dsid}-{lg[CLDF_ID]}'
                lg['Dataset'] = dsid

            ds_concepts = {
                concept[CLDF_ID]: concept
                for concept in ds.iter_rows(
                    'ParameterTable',
                    CLDF_ID,
                    CLDF_CONCEPTICON_ID,
                    'Concepticon_Gloss')
                # we only want number concepts
                if concept['Concepticon_Gloss'] in concepts}
            ds_forms = [
                form
                for form in ds.iter_rows(
                    'FormTable',
                    CLDF_ID,
                    CLDF_LANGUAGE_ID,
                    CLDF_PARAMETER_ID,
                    CLDF_FORM,
                    CLDF_VALUE,
                    CLDF_COMMENT)
                if form[CLDF_PARAMETER_ID] in ds_concepts]
            for form in ds_forms:
                form[CLDF_LANGUAGE_ID] = ds_languages[form[CLDF_LANGUAGE_ID]][CLDF_ID]
                ds_concept = ds_concepts[form[CLDF_PARAMETER_ID]]
                form[CLDF_PARAMETER_ID] = slug(ds_concept['Concepticon_Gloss'])
                form['Concepticon_Gloss'] = ds_concept['Concepticon_Gloss']

            languages.update(
                (lg[CLDF_ID], lg)
                for lg in ds_languages.values())
            forms.extend(ds_forms)

        # get base info from the external document
        args.log.info('Loading base info')
        base_info = {}
        for row in self.etc_dir.read_csv('bases.tsv', delimiter='\t', dicts=True):
            if row['Annotator'] == 'Russell Barlow':
                row['Comment'] = ''
            if row['Language_ID']:
                base_info[row['Language_ID']] = row
            else:
                base_info[row['Glottocode']] = row

        one_to_infinity = {
            concept['CONCEPTICON_GLOSS']
            for concept in concepts.values()}
        one_to_forty = {
            concept['CONCEPTICON_GLOSS']
            for concept in concepts.values()
            if concept['TEST'] in {'1', '2'}}
        one_to_thirty = {
            concept['CONCEPTICON_GLOSS']
            for concept in concepts.values()
            if concept['TEST'] == '1'}
        coverage_all = coverage(forms, one_to_infinity)
        coverage_one_to_forty = coverage(forms, one_to_forty)
        coverage_one_to_thirty = coverage(forms, one_to_thirty)

        selected_languages = [
            language
            for language in sorted(
                languages.values(),
                key=lambda lg: coverage_all.get(lg[CLDF_ID], 0),
                reverse=True)
            if language.get(CLDF_GLOTTOCODE)
            # skip lote1237-9 which doesn't have data in the original dataset either
            and language[CLDF_ID] != 'barlowpacific-lote1237-9'
        ]
        selected_languages.sort(key=lambda lg: lg['Glottocode'])
        # make sure we only have languages with data points in there
        assert all(coverage_all.get(lg[CLDF_ID], 0) > 0 for lg in selected_languages)

        args.log.info('Processing %d selected concepts', len(concepts))
        for concept in concepts.values():
            args.writer.add_concept(
                ID=slug(concept['CONCEPTICON_GLOSS']),
                Name=concept['CONCEPTICON_GLOSS'],
                Concepticon_ID=concept['CONCEPTICON_ID'],
                Concepticon_Gloss=concept['CONCEPTICON_GLOSS'],
            )

        # how to represent basic relations in Chan, which are frequent enough
        # in the data
        target_bases = {
            'Decimal': 'decimal',
            'decimal': 'decimal',
            'Decimal-Vigesimal': 'decimal/vigesimal',
            'Vigesimal': 'vigesimal',
            'Restricted': 'restricted',
            'vigesimal': 'vigesimal',
            'quinary': 'quinary',
            'quinary AND decimal': 'quinary',
            'quinary AND vigesimal': 'quinary',
            'quinary AND decimal AND vigesimal': 'quinary',
            'binary': 'binary',
            'decimal AND vigesimal': 'decimal/vigesimal',
            'decimal OR vigesimal': 'decimal/vigesimal',
            'duodecimal': 'duodecimal',
            'octal': 'octal',
            'quinary OR decimal': 'quinary/decimal',
            'quinary AND vigesimal OR decimal': 'quinary/vigesimal',
            'quinary AND double decimal': 'quinary/decimal',
            'octal AND decimal': 'octal',
            'octal AND duodecimal AND hexadecimal AND vigesimal AND tetravigesimal': 'octal',
            'octogesimal': 'octogesimal',
            'trigesimal': 'trigesimal',
            'quinquagesimal': 'quinquagesimal',
            'pentadecimal OR pentavigesimal': 'pentadecimal/pentavigesimal',
            'pentavigesimal': 'pentavigesimal',
        }

        valid_bases = {
            'binary',
            'decimal',
            'mixed',
            'decimal/vigesimal',
            'duodecimal',
            'octal',
            'octogesimal',
            'pentadecimal/pentavigesimal',
            'pentavigesimal',
            'quaternary',
            'quinary',
            'quinary/decimal',
            'quinquagesimal',
            'restricted',
            'senary',
            'trigesimal',
            'vigesimal',
        }

        glosses = collect_glosses(self.etc_dir.joinpath('Merging').read_csv(
            'data.glossed.checked.filtered.csv',
            dicts=True))

        base_errors = set()
        args.log.info('Processing %d selected languages', len(selected_languages))
        for language in selected_languages:
            # check for sufficient coverage
            language_id = language[CLDF_ID]
            glottocode = language[CLDF_GLOTTOCODE]
            language_dataset = language['Dataset']

            # retrieve annotated base
            if language_id in base_info:
                annotated_base, annotator, cmt = (
                    target_bases.get(
                        base_info[language_id]['Base'], base_info[language_id]['Base'],
                    ),
                    base_info[language_id]['Annotator'],
                    base_info[language_id]['Comment'],
                )
            elif glottocode in base_info:
                annotated_base, annotator, cmt = (
                    target_bases.get(
                        base_info[glottocode]['Base'],
                        base_info[glottocode]['Base'],
                    ),
                    base_info[glottocode]['Annotator'],
                    base_info[glottocode]['Comment'],
                )
            elif language_dataset == 'numerals':
                annotated_base = target_bases.get(language['Base'], language['Base'])
                annotator, cmt = 'Eugene Chan', ''
            elif language_dataset == 'sand':
                annotated_base = target_bases.get(language['Base'], language['Base'])
                annotator, cmt = 'Mamta Kumari', ''
            else:
                annotated_base, annotator, cmt = '', '', ''

            # check for type
            if annotated_base and annotated_base not in valid_bases:
                if annotated_base.lower() != 'unknown':
                    base_errors.add((language_id, annotated_base, annotator))
                annotated_base, annotator, cmt = '', '', ''

            if (language_comment := language.get('Comment')):
                cmt = f'{cmt}; {language_comment}' if cmt else language_comment

            args.writer.add_language(
                ID=language_id,
                Name=language[CLDF_NAME],
                Dataset=language['Dataset'],
                Glottocode=language[CLDF_GLOTTOCODE],
                Latitude=language[CLDF_LATITUDE],
                Longitude=language[CLDF_LONGITUDE],
                Macroarea=language[CLDF_MACROAREA],
                BaseAnnotation=annotated_base,
                BaseAnnotator=annotator,
                BaseComment=cmt,
                Coverage=coverage_all.get(language_id, 0),
                OneToThirty=coverage_one_to_thirty.get(language_id, 0),
            )

        selected_language_ids = {lg[CLDF_ID] for lg in selected_languages}
        selected_forms = [
            form for form in forms if form[CLDF_LANGUAGE_ID] in selected_language_ids]
        args.log.info('Processing %d selected forms', len(selected_forms))
        for form in selected_forms:
            language_id = form[CLDF_LANGUAGE_ID]
            language = languages[language_id]
            concept = concepts[form['Concepticon_Gloss']]
            concept_id = slug(concept['CONCEPTICON_GLOSS'])
            language_dataset = language['Dataset']
            source, _ = datasets[language_dataset]
            gloss_key = GlossKey(
                language_id=language_id,
                parameter_id=concept_id,
                value=form[CLDF_VALUE])
            gloss = glosses.get(gloss_key) or {}
            glossed_form = ChainMap(gloss, form)

            # we all love R...
            gloss = glossed_form.get('Gloss')
            assert gloss != 'NA'
            gloss_clean = glossed_form.get('Gloss.clean')
            assert gloss_clean != 'NA'
            gloss_math = glossed_form.get('Gloss.math')
            assert gloss_math != 'NA'
            gloss_calc = glossed_form.get('Gloss.calc')
            assert gloss_calc != 'NA'
            alternate_gloss = glossed_form.get('Alternate_gloss')
            if alternate_gloss == 'NA':
                alternate_gloss = ''
            comment_glosser = glossed_form.get('Comment_glosser')
            if comment_glosser == 'NA':
                comment_glosser = ''

            args.writer.add_form(
                Language_ID=language_id,
                Parameter_ID=concept_id,
                Value=glossed_form[CLDF_VALUE],
                Form=simple_chars(glossed_form[CLDF_FORM]),
                Loan=glossed_form['Loan'],
                Source=source,
                NumberValue=concept['NUMBER_VALUE'],
                Comment=glossed_form['Comment'].strip() if glossed_form.get('Comment') else None,
                Gloss=gloss,
                GlossClean=gloss_clean,
                GlossMath=gloss_math,
                GlossCalc=gloss_calc,
                AlternateGloss=alternate_gloss,
                CommentGlosser=comment_glosser,
            )

        counts = defaultdict(int)
        with open(self.dir / 'base_errors.md', 'w') as f:
            f.write('Language | Annotation | Annotator\n--- | --- | ---\n')
            for language_id, base, annotator in sorted(base_errors):
                f.write(f'{language_id} | {base} | {annotator}\n')
                counts[base, annotator] += 1

        for (base, annotator), count in counts.items():
            args.log.info(
                'Problematic annotation %-40s by %-20s occurs %d times',
                base, annotator, count)
