
import json

from typing import Optional
from typing import List

from sqlalchemy     import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from uuid import uuid4 as uuid

from flask_app import db

from . import docsTable
from . import assetsTable
from . import ln_docs_tags

from src.models.tags import Tags

from src.utils.mixins import MixinTimestamps
from src.utils.mixins import MixinExistsID
from src.utils.mixins import MixinFieldMergeable
from src.utils.mixins import MixinByIds

from src.schemas.serialization import SchemaSerializeDocs


_err, _dbcli = db

_schemaDocsDump     = SchemaSerializeDocs()
_schemaDocsDumpMany = SchemaSerializeDocs(many = True)


# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes
class Docs(MixinTimestamps, MixinExistsID, MixinByIds, MixinFieldMergeable, _dbcli.Model):
  __tablename__ = docsTable

  id   : Mapped[int]           = mapped_column(primary_key = True)
  key  : Mapped[Optional[str]] = mapped_column(default = uuid)
  data : Mapped[dict]          = mapped_column(JSON)

  # foreign key
  asset_id = mapped_column(_dbcli.ForeignKey(f'{assetsTable}.id'))
  
  # virtual
  tags  : Mapped[List['Tags']] = relationship(secondary = ln_docs_tags, back_populates = 'docs')
  asset : Mapped['Assets']     = relationship(back_populates = 'docs')

  
  # magic
  def __repr__(self):
    return f'Docs({json.dumps(self.dump())})'
  

  # public
  def get_data(self, updates = None):
    d = self.data.copy()
    if None != updates:
      d.update(updates)
    return d
  
  
  # public
  def dump(self, **kwargs):
    return _schemaDocsDump.dump(self, **kwargs)
  

  @staticmethod
  def dicts(docs, **kwargs):
    return _schemaDocsDumpMany.dump(docs, **kwargs)      
  
  
  @staticmethod
  def by_key(key, *, create = False, _commit =  True):
    d = None
    if key:
      d = _dbcli.session.scalar(
        _dbcli.select(
          Docs
        ).where(
          Docs.key == key
        ))
      
      if not d:
        if True == create:
          # @create:default
          d = Docs(data = {}, key = key)
          _dbcli.session.add(d)
          if _commit:
            _dbcli.session.commit()
    
    return d
  

  @staticmethod
  def tagged(tag_name):
    return _dbcli.session.scalars(
      _dbcli.select(
        Docs
      ).join(
        Docs.tags
      ).where(
        Tags.tag == tag_name
      ))


  @staticmethod
  def by_tag_and_id(tag, id):
    return _dbcli.session.scalar(
      _dbcli.select(
        Docs
      ).join(
        Docs.tags
      ).where(
          Tags.tag == tag,
          Docs.id  == id,
      ))


