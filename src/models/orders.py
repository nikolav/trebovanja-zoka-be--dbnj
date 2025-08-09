
from enum import Enum

from typing import Optional
from typing import List

from uuid import uuid4 as uuid

from sqlalchemy     import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.utils.mixins import MixinTimestamps
from src.utils.mixins import MixinIncludesTags
from src.utils.mixins import MixinByIds
from src.utils.mixins import MixinExistsID
from src.utils.mixins import MixinFieldMergeable

from . import db
from . import assetsTable
from . import ordersTable
from . import ln_orders_tags
from . import ln_orders_products

from .tags import Tags


_err, _dbcli = db


class OrdersIOEvents(Enum):
  IOEVENT_ORDERS_CONFIGRED_prefix = 'IOEVENT_ORDERS_CONFIGRED:b6c6caf1-9be2-57a5-9ba0-6254e59d6909:'


class OrdersTags(Enum):
  TAG_ORDERS_SHAREABLE_GLOBALY = 'TAG_ORDERS_SHAREABLE_GLOBALY:61cde3f6-cdf8-5769-bf11-93b91f4ff49d'


class Orders(MixinTimestamps, MixinIncludesTags, MixinByIds, MixinExistsID, MixinFieldMergeable, _dbcli.Model):
  __tablename__ = ordersTable

  # ID
  id: Mapped[int] = mapped_column(primary_key = True)

  # fields
  key    : Mapped[Optional[str]] = mapped_column(default = uuid)
  status : Mapped[Optional[str]]
  data   : Mapped[Optional[dict]] = mapped_column(JSON)
  notes  : Mapped[Optional[str]]
  
  # .sid related asset:site
  site_id = mapped_column(_dbcli.ForeignKey(f'{assetsTable}.id'))

  # virtual
  # related asset:site
  site     : Mapped['Assets']       = relationship(back_populates = 'site_orders')
  tags     : Mapped[List['Tags']]   = relationship(secondary = ln_orders_tags,     back_populates = 'orders')
  products : Mapped[List['Assets']] = relationship(secondary = ln_orders_products, back_populates = 'orders')
  

  # public
  def tags_add(self, *tags, _commit = True):
    changes = 0

    for tname in filter(lambda p: not self.includes_tags(p), tags):
      tp = Tags.by_name(tname, create = True, _commit = _commit)
      tp.orders.append(self)
      changes += 1
    
    if (0 < changes) and (True == _commit):
      _dbcli.session.commit()
    
    return changes
  
  
  # public
  def tags_rm(self, *tags, _commit = True):
    changes = 0

    for tname in filter(lambda p: self.includes_tags(p), tags):
      tp = Tags.by_name(tname, create = True, _commit = _commit)
      tp.orders.remove(self)
      changes += 1
    
    if (0 < changes) and (True == _commit):
      _dbcli.session.commit()
    
    return changes


