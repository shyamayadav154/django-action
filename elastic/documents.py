from django_elasticsearch_dsl import (
    Document ,
    fields,
    Index,
)
from django_elasticsearch_dsl.registries import registry
from resume.models import CandidatePrivateData, MiscDetail, WorkDetail,CandidateEducation,Elastic_demo
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from elasticsearch_dsl import analyzer, tokenizer

autocomplete_analyzer = analyzer('autocomplete_analyzer',
            tokenizer=tokenizer('trigram', 'nGram', min_gram=1, max_gram=20),
            filter=['lowercase']
    )
 
# PUBLISHER_INDEX = Index('candidate_education')

# PUBLISHER_INDEX.settings(
#     number_of_shards=1,
#     number_of_replicas=1
# )

# PUBLISHER_INDEX1 = Index('work_detail')

# PUBLISHER_INDEX1.settings(
#     number_of_shards=1,
#     number_of_replicas=1
# )

# PUBLISHER_INDEX2 = Index('misc_detail')

# PUBLISHER_INDEX2.settings(
#     number_of_shards=1,
#     number_of_replicas=1,
#     max_ngram_diff= 20
# )

# custom_stop_words = token_filter(
#     'custom_stopwords',
#     type='stop',
#     ignore_case=True,
#     stopwords=['the', 'and']

# )


# html_strip = analyzer(
#     'html_strip',
#     tokenizer="standard",
#     filter=["lowercase", "asciifolding", custom_stop_words],
#     char_filter=["html_strip"],
# )


# html_strip = analyzer(
#     'html_strip',
#     tokenizer="keyword",
#     filter=["standard", "lowercase", "stop", "snowball"],
#     char_filter=["html_strip"]
# )

# @PUBLISHER_INDEX.doc_type
@registry.register_document
class CandidateEducationDocument(Document):
    
    id = fields.IntegerField()
    start_year = fields.IntegerField()
    end_year= fields.IntegerField()
    # fielddata=True
    degree = fields.ObjectField(properties={"name": fields.TextField()})
    college_name = fields.TextField(
        # analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer = 'keyword' ),
            'suggest': fields.CompletionField(),
        }
    )
    # access = fields.ObjectField(
    #     properties={"id": fields.TextField()}
    # )
    access= fields.ObjectField(
        properties={"id": fields.TextField(
            fields={'raw': fields.KeywordField()},
                   analyzer="keyword"
        )}
    )
    class Index:
        name = "cand_edu"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'max_ngram_diff': 20 # This seems to be important due to the constraint for max_ngram_diff beeing 1
        }

    class Django(object):
        model = CandidateEducation

# @registry.register_document
# @PUBLISHER_INDEX1.doc_type
@registry.register_document
class OnlySearchWorkdetailDocument(Document):
    id = fields.IntegerField()
    sub_skills = fields.ObjectField(
        properties={"name": fields.TextField(
            # analyzer=autocomplete_analyzer,
            fields={
                    'raw': KeywordField(),#fields.TextField(),#
                    'suggest': fields.CompletionField(),
                }
        )}
    )
    skills = fields.ObjectField(
            properties={'name': fields.TextField(
                analyzer=autocomplete_analyzer,
                # analyzer=html_strip,
                fields={
                    'raw': fields.TextField(),#KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )
        }
        )
    
    resp_title = fields.ObjectField(properties={"name": fields.TextField(
        # analyzer=autocomplete_analyzer,
        fields={
                    'raw':fields.TextField(),#KeywordField(),
                    'suggest': fields.CompletionField(),
                }
    )})
    
    # access = fields.ObjectField(
    #     properties={"id": fields.TextField()}
    # )
    access= fields.ObjectField(
        properties={"id": fields.TextField(
            fields={'raw': fields.KeywordField()},
                   analyzer="keyword"
        )}
    )

    company_name=fields.TextField(
        # analyzer=autocomplete_analyzer,
    )

    my_tasks=fields.TextField(
        # analyzer=autocomplete_analyzer,
    )
    class Index:
        name = "work_detail"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'max_ngram_diff': 20 # This seems to be important due to the constraint for max_ngram_diff beeing 1
        }

    class Django(object):
        model = WorkDetail
        

from elasticsearch_dsl import analyzer, tokenizer

autocomplete_analyzer = analyzer('autocomplete_analyzer',
            tokenizer=tokenizer('trigram', 'nGram', min_gram=1, max_gram=20),
            filter=['lowercase']
        )

@registry.register_document
class MiscdetailDocument(Document):
   
    id = fields.IntegerField()

    job_title = fields.ObjectField(
            properties={'name': fields.TextField(
                # required=True,
                analyzer=autocomplete_analyzer,
                fields={
                    'raw': fields.TextField(),#KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )
        }
        )

    open_to = fields.ObjectField(
            properties={'name': fields.TextField(
                # required=True,
                analyzer=autocomplete_analyzer,
                fields={
                    'raw': fields.TextField(),#KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )
        }
        )

    status = fields.ObjectField(
            properties={'name': fields.TextField(
                # required=True,
                analyzer=autocomplete_analyzer,
                fields={
                    'raw': fields.TextField(),#KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )
        }
        )

    current_city = fields.ObjectField(
            properties={'name': fields.TextField(
                # required=True,
                analyzer=autocomplete_analyzer,
                fields={
                    'raw': fields.TextField(),#KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )
        }
        )

    locations = fields.TextField(#required=True,
                    analyzer=autocomplete_analyzer)

    # access = fields.ObjectField(
    #     properties={"id": fields.TextField()}
    # )
    access= fields.ObjectField(
        properties={"id": fields.TextField(
            fields={'raw': fields.KeywordField()},
                   analyzer="keyword"
        )}
    )

    class Index:
        name = "misc_detail"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'max_ngram_diff': 20 # This seems to be important due to the constraint for max_ngram_diff beeing 1
        }

    class Django(object):
        model = MiscDetail
    

@registry.register_document
class PrivateDataDocument(Document):

    id = fields.IntegerField()
    name = fields.TextField(
        fields={'raw': fields.KeywordField()},
                   analyzer="keyword")
    # phone_no=fields.LongField()
    current_salary = fields.LongField()
    expected_salary = fields.LongField()
    notice_time = fields.IntegerField()
    access= fields.ObjectField(
        properties={"id": fields.TextField(
            fields={'raw': fields.KeywordField()},
                   analyzer="keyword"
        )}
    )
    class Index:
        name = "private_data"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'max_ngram_diff': 20 # This seems to be important due to the constraint for max_ngram_diff beeing 1
        }

    class Django(object):
        model = CandidatePrivateData

# @registry.register_document
# class ElasticdemoDocument(Document):
#     # name = fields.TextField(
#     #     fields={
#     #         'raw':{
#     #             'type': 'keyword',
#     #         }
            
#     #     }
#     # )
#     # age = fields.TextField(
#     #     fields={
#     #         'raw':{
#     #             'type': 'keyword',
#     #         }
            
#     #     }
#     # )
#     # school= fields.TextField(
#     #     fields={
#     #         'raw':{
#     #             'type': 'keyword',
#     #         }
            
#     #     }
#     # )
#     # location= fields.TextField(
#     #     fields={
#     #         'raw':{
#     #             'type': 'keyword',
#     #         }
            
#     #     }
#     # )
#     class Index:
#         name = "demo"

#     class Django(object):
#         model = Elastic_demo
#         fields = [
#             "id",
#             "name",
#             "age",
#             "school",
#             "location"
#         ]
