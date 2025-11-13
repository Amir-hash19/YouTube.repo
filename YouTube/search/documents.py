from django_elasticsearch_dsl import Document, Index, fields
from channle.models import Channel



channel_index = Index('channels')



@channel_index.document
class ChannelDocument(Document):

    owner = fields.ObjectField(properties={
        'username': fields.TextField(),
        'email': fields.TextField(),
    })

    class Django:
        model = Channel
        fields = [
            "title",
            "channel_id",
            "bio"
        ]







