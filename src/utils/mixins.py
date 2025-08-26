
from datetime import datetime
from datetime import timezone
from copy     import deepcopy

from sqlalchemy     import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from flask_app import db

from src.models.tags            import Tags
from src.utils.merge_strategies import dict_deepmerger_extend_lists as merger


_err, _dbcli = db


class MixinTimestamps():
  created_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(tz = timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(tz = timezone.utc),
                                               onupdate = lambda: datetime.now(tz = timezone.utc))


class MixinExistsID():
  @classmethod
  def id_exists(cls, id):
    return 0 < _dbcli.session.scalar(
      _dbcli.select(
        func.count(cls.id)
      ).where(
        cls.id == id
      )
    )


class MixinByIds():
  @classmethod
  def by_ids(cls, *ids):
    q = _dbcli.select(
        cls
      ).where(
        cls.id.in_(ids))
    return _dbcli.session.scalars(q)


class MixinFieldMergeable():
  def data_patched(self, *, patch, FIELD = 'data'):
    return merger.merge(deepcopy(getattr(self, FIELD, {})), patch)
  
  def data_update(self, *, patch, FIELD = 'data'):
    setattr(self, FIELD, patch)


class MixinIncludesTags():
  # public
  def includes_tags(self, *args, ANY = False):
    tags_self = [t.tag for t in self.tags]
    return all(tag in tags_self for tag in args) if True != ANY else any(tag in tags_self for tag in args)


class MixinByIdsAndType():
  @classmethod
  def by_ids_and_type(cls, *ids, type = None):
    q = _dbcli.select(
        cls
      ).where(
        cls.id.in_(ids)
      )
    if None != type:
      q = q.where(
          type == cls.type
        )
    
    return _dbcli.session.scalars(q)


class MixinManageTagsBase():
  FIELD = None
  # public
  def tags_add(self, *tags, _commit = True):
    changes = 0

    for tname in filter(lambda p: not self.includes_tags(p), tags):
      tp = Tags.by_name(tname, create = True, _commit = _commit)
      getattr(tp, self.FIELD).append(self)
      changes += 1
    
    if (0 < changes) and (True == _commit):
      _dbcli.session.commit()
    
    return changes
  
  
  # public
  def tags_rm(self, *tags, _commit = True):
    changes = 0

    for tname in filter(lambda p: self.includes_tags(p), tags):
      tp = Tags.by_name(tname, create = True, _commit = _commit)
      getattr(tp, self.FIELD).remove(self)
      changes += 1
    
    if (0 < changes) and (True == _commit):
      _dbcli.session.commit()
    
    return changes


class MixinManageTagsOnOrders(MixinManageTagsBase):
  FIELD = 'orders'


class MixinManageTagsOnAssets(MixinManageTagsBase):
  FIELD = 'assets'


class MixinManageTagsOnDocs(MixinManageTagsBase):
  FIELD = 'docs'


