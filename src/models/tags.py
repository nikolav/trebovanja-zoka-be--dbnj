
from typing import List
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from flask_app import db

from . import tagsTable
from . import ln_docs_tags
from . import ln_assets_tags
from . import ln_orders_tags


_err, _dbcli = db

# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes
class Tags(_dbcli.Model):
  __tablename__ = tagsTable

  id: Mapped[int] = mapped_column(primary_key = True)

  tag        : Mapped[str] = mapped_column(unique = True)
  description: Mapped[Optional[str]]

  # virtual
  docs   : Mapped[List['Docs']]   = relationship(secondary = ln_docs_tags,   back_populates = 'tags')
  assets : Mapped[List['Assets']] = relationship(secondary = ln_assets_tags, back_populates = 'tags')
  orders : Mapped[List['Orders']] = relationship(secondary = ln_orders_tags, back_populates = 'tags')


  # magic
  def __repr__(self):
    return f'Tags(id={self.id!r}, tag={self.tag!r})'
  

  # magic
  def __str__(self):
    # return super().__str__()
    return self.tag


  @staticmethod
  def by_name(tag_name, *, create = False, _commit = True):
    tag = None

    try:
      tag = _dbcli.session.scalar(
        _dbcli.select(
          Tags
        ).where(
          Tags.tag == tag_name
        ))
      
      if not tag:
        if True == create:
          tag = Tags(tag = tag_name)
          _dbcli.session.add(tag)
          if _commit:
            _dbcli.session.commit()

    except Exception as e:
      raise e
        
    return tag
