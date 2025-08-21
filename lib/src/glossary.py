import json
import glob
from pathlib import Path
from extractor import *
from typing import Callable

def load_chapters(path : str) -> dict[str, str]:
    """Loads all chapters matching path into a dictionary
        chapter_name : chapter_content

    Args:
        path: glob pattern for chapters
    """
    chapters = {}
    file_paths = glob.glob(path)
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            p = Path(file_path)
            content = file.read()
            chapter_name = p.name
            chapters[chapter_name] = content
    return chapters

class GlossaryBuilder:
    """Object that builds a glossary given a list of chapters in a dictionary format
        chapter_name : chapter_content
    
    Args:
        extractor: Extractor object to extract named entities from text
        entity_filter: [Optional] callable that filters entity objects
        chapter_name_to_num:  [Optional] callable that converts chapter names to numbers
        normalizer: [Optional] callable that normalizes a named entity
    """
    def __init__(self, extractor : Extractor, entity_filter : Callable[[dict], bool] = None, \
                 chapter_name_to_num : Callable[[str], int] = None, normalizer : Callable[[str], str] = None):
        self.extractor = extractor
        self.entity_filter = entity_filter
        self.chapter_name_to_num = chapter_name_to_num
        self.normalizer = normalizer or (lambda x : x)
    
    def preprocess(self, chapters : dict[str, str], wordy = False) -> dict[str, dict]:
        """Return a dictionary in the format
            chapter_number : 
                {
                    'chapter_name' : ...
                    'entities' : [list of named entities in chapter]
                }

        Args:
            wordy: enable/disable log messages
        """
        if wordy:
            print("Preprocessing chapters")
        chap_ent_dict = {}
        for index, chapter_name in enumerate(chapters):
            if wordy:
                print(f"Processing chapter {chapter_name}")
            if self.chapter_name_to_num:
                chapter_num = self.chapter_name_to_num(chapter_name)
            else:
                chapter_num = index
            if chapter_num in chap_ent_dict:
                raise Exception("Duplicate chapter number")
            chap_ent_dict[chapter_num] = {'chapter_name' : chapter_name, 'entities' : []}
            ents = self.extractor.extract_named_entities(chapters[chapter_name])
            for ent in ents:
                if self.entity_filter and self.entity_filter(ent):
                    continue
                normalized = self.normalizer(ent['word'])
                chap_ent_dict[chapter_num]['entities'].append(normalized)
        if wordy:
            print("Done preprocessing")
        return chap_ent_dict

    def keep_first_appearances(self, preprocessed : dict[str, dict]) -> dict[str, dict]:
        """Given a preprocessed glossary, filter out all entities except their first appearances
        
        Args:
            preprocessed: a preprocessed glossary
        """
        seen = set()
        sorted_keys = sorted(list(preprocessed.keys()))
        first_appearances = {}
        for chapter_num in sorted_keys:
            chapter_entities = preprocessed[chapter_num]['entities']
            for entity in chapter_entities:
                if entity not in seen:
                    if chapter_num not in first_appearances:
                        first_appearances[chapter_num] = {
                            'chapter_name' : preprocessed[chapter_num]['chapter_name'],
                            'entities' : []
                        }
                    first_appearances[chapter_num]['entities'].append(entity)
        return first_appearances


def convert_chapter_underscore_num(chapter_name : str) -> int:
    """Converts a chapter name of the form chapter_[chapter_num].txt to chapter_num"""
    return int(chapter_name[8:-4])

def filter_by_score(entity : dict, min_score : int) -> bool:
    """Filters entity of the form
        {
            'entity_group' : ...
            'score' : ...
            'word' : ...
            'start' : ...
            'end' : ...
        }
        by minimum score
    """
    return True if entity['score'] >= min_score else False

def remove_space(word : str) -> str:
    """Remove all spaces in word and strip"""
    return word.replace(' ', '').strip()