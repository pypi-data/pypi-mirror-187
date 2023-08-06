import json

from fuzzywuzzy import fuzz
from utils import SECONDS_IN, String, cache, hashx

from gig.core.EntBase import EntBase
from gig.core.EntType import EntType
from gig.core.GIGTable import GIGTable


class Ent(EntBase):
    def to_json(self):
        return json.dumps(self.d)

    @staticmethod
    def from_json(json_str):
        d = json.loads(json_str)
        return Ent(d)

    @staticmethod
    def from_dict(d):
        d = d.copy()
        if 'area' in d:
            d['area'] = String(d['area']).float

        if 'population' in d:
            d['population'] = String(d['population']).int

        if 'centroid_altitude' in d:
            try:
                d['centroid_altitude'] = String(d['centroid_altitude']).float
            except ValueError:
                d['centroid_altitude'] = 0

        for k in ['centroid', 'subs', 'supers', 'ints', 'eqs']:
            if k in d:
                if d[k]:
                    d[k] = json.loads(d[k].replace('\'', '"'))
        return Ent(d)

    @staticmethod
    def load_list_for_type(ent_type: EntType) -> list:
        d_list = ent_type.remote_data_list
        ent_list = [Ent.from_dict(d) for d in d_list]
        return ent_list

    @staticmethod
    def load_idx_for_type(ent_type: EntType) -> dict:
        ent_list = Ent.load_list_for_type(ent_type)
        ent_idx = {ent.id: ent for ent in ent_list}
        return ent_idx

    @staticmethod
    def load_for_id(id: str):
        ent_type = EntType.from_id(id)
        ent_idx = Ent.load_idx_for_type(ent_type)
        return ent_idx[id]

    @staticmethod
    def load_list_for_id_list(id_list: list) -> list:
        ent_list = [Ent.load_for_id(id) for id in id_list]
        return ent_list

    @staticmethod
    def load_ids_for_type(ent_type: EntType) -> list:
        ent_list = Ent.load_list_for_type(ent_type)
        id_list = [ent.id for ent in ent_list]
        return id_list

    @staticmethod
    def load_list_by_name_fuzzy(
        name_fuzzy: str,
        filter_ent_type: EntType = None,
        filter_parent_id: str = None,
        limit: int = 5,
        min_fuzz_ratio: int = 80,
    ) -> list:

        cache_key = hashx.md5(
            '.'.join(
                [
                    name_fuzzy,
                    filter_ent_type.name if filter_ent_type else str(None),
                    str(filter_parent_id),
                    str(limit),
                    str(min_fuzz_ratio),
                ]
            )
        )

        @cache(cache_key, SECONDS_IN.WEEK)
        def inner():
            ent_and_ratio_list = []
            for entity_type in EntType.list():
                if filter_ent_type and (filter_ent_type != entity_type):
                    continue

                ent_list_for_type = Ent.load_list_for_type(entity_type)
                for ent in ent_list_for_type:
                    if filter_parent_id and ent.is_parent_id(
                        filter_parent_id
                    ):
                        continue

                    fuzz_ratio = fuzz.ratio(ent.name, name_fuzzy)

                    if fuzz_ratio >= min_fuzz_ratio:
                        ent_and_ratio_list.append([ent, fuzz_ratio])

            ent_list = [
                item[0]
                for item in sorted(ent_and_ratio_list, key=lambda x: -x[1])
            ]

            if len(ent_list) >= limit:
                ent_list = ent_list[:limit]

            return [ent.to_json() for ent in ent_list]

        return [Ent.from_json(x) for x in inner()]

    def gig(self, gig_table: GIGTable):
        return gig_table.get(self.id)
