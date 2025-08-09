
from typing   import List
from typing   import Optional
from enum     import Enum
from uuid     import uuid4 as uuid

from sqlalchemy     import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy.orm import aliased
# from sqlalchemy import event

from flask_app import db
# from flask_app import io

from . import assetsTable
from . import ln_assets_tags
from . import ln_assets_assets
from . import ln_orders_products

from src.utils.mixins import MixinTimestamps
from src.utils.mixins import MixinByIds
from src.utils.mixins import MixinExistsID
from src.utils.mixins import MixinFieldMergeable
from src.utils.mixins import MixinIncludesTags
from src.utils.mixins import MixinByIdsAndType

from src.models.docs  import Docs
from src.models.docs  import Tags

from src.config       import Config
from src.utils.unique import Unique

from src.schemas.serialization import SchemaSerializeAssetsTextSearch


_err, _dbcli = db

class AssetsType(Enum):
  # DIGITAL = "Digital Asset"
  #  communicate announcements; users can not comment in channels
  DIGITAL_CHANNEL = 'DIGITAL_CHANNEL:YqmefT'
  #  custom commnication for users
  DIGITAL_CHAT = 'DIGITAL_CHAT:4nASbEj8pFvqm'
  DIGITAL_FORM = 'DIGITAL_FORM:TzZJs5PZqcWc'
  DIGITAL_POST = 'DIGITAL_POST:6b9959a1-a82c-54a6-b7b2-dbeb285f23d7'
  # all users access
  DIGITAL_CHANNEL_GLOBAL = 'DIGITAL_CHANNEL_GLOBAL:tQ6c5O1mRDtP6fDCCj'
  DIGITAL_CHAT_GLOBAL    = 'DIGITAL_CHAT_GLOBAL:JS4nzSghZq4CZH'
  DIGITAL_FORM_GLOBAL    = 'DIGITAL_FORM_GLOBAL:DKp32J'

  # GROUP = "Group Asset"
  PEOPLE_GROUP_TEAM = 'PEOPLE_GROUP_TEAM:sEdkj9r'

  # PHYSICAL = "Physical Asset"
  PHYSICAL_PRODUCT           = 'PHYSICAL_PRODUCT:u1zDoNxQnYLnHHbp'
  PHYSICAL_STORE             = 'PHYSICAL_STORE:5btoy9I8IKgT0RJO'
  PHYSICAL_DISTRIBUTION_UNIT = 'PHYSICAL_DISTRIBUTION_UNIT:3e854289-02e2-5aa8-85ec-e9d1fc021ea7'

  # DIGITAL_TASKS
  DIGITAL_TASKS = 'DIGITAL_TASKS:5373aab3-2b75-5b19-abcb-419fbf2ffd6f'
  
  # FINANCIAL = "Financial Asset"

  # ISSUES
  ISSUE_GENERAL = 'ISSUE_GENERAL:x53CJbY'

# class AssetsDigitalFormFieldTypes(Enum):
#   # asset.data
#   #   {
#   #     fields: [
#   #       {
#   #         data { question, description, required:bool, multiple:bool },
#   #         items: string[],
#   #         key,
#   #         type
#   #       },
#   #     ]
#   #   }
  
#   # @choice: 
#   #   .question .description? .required .items: { title:string; value: any; }[] .multiple?
#   CHOICE  = 'DIGITAL_FORM:CHOICE:hrNoq9hhbh2wUyZ9fjmf'
#   # @text
#   #   .question .description? .required
#   TEXT    = 'DIGITAL_FORM:TEXT:54QNKF'
#   # @boolean
#   #   .question .description? .required
#   BOOLEAN = 'DIGITAL_FORM:BOOLEAN:P1cUlYS4'
#   # @rating
#   #   .question .description? .required
#   RATING  = 'DIGITAL_FORM:RATING:C6zX66WEWk'
#   # @files
#   #   .question .description? .required
#   FILES   = 'DIGITAL_FORM:FILES:KBr3gZuJAM4s'
#   # @table, fill table data
#   TABLE_DATA = 'DIGITAL_FORM:TABLE_DATA:GOOGLE_SHEETS:1lbH5rK'
#   # @goog.forms, complete google form
#   GOOGLE_FORMS = 'DIGITAL_FORM:GOOGLE_FORMS:NWso2XvdHbLlCIW4Q9'


class AssetsStatus(Enum):
  ACTIVE    = 'ACTIVE:YjCrzsLhGtiE4f3ffO'
  ARCHIVED  = 'ARCHIVED:zfbooZxI5IXQmbZIZ'
  CANCELED  = 'CANCELED:2whyBKhy6vv98bPcsUNc'
  CLOSED    = 'CLOSED:bGbGsEnAk2xu9sye7'
  DONE      = 'DONE:6jRIWy6fWT3mT3uNuF2'
  INACTIVE  = 'INACTIVE:fdHJBPHGyC'
  PENDING   = 'PENDING:P4kOFE3HF'

  POSTS_BLOCKED = 'POSTS_BLOCKED:UcAMV'
  POSTS_OPEN    = 'POSTS_OPEN:luIlZa5'


class AssetsCondition(Enum):
  BAD            = 'BAD:oKRchSYlnm8lMqcqoq'
  DEPRECATED     = 'DEPRECATED:stuDFLe7AQf4eKr0RVIn'
  GOOD           = 'GOOD:xW3qMs2e94T9S'
  NEEDS_REPAIR   = 'NEEDS_REPAIR:NJGJD8Spq9A2aFrQgas'
  OUT_OF_SERVICE = 'OUT_OF_SERVICE:KpJUn2IqM2oj'


class AssetsIOEvents(Enum):
  UPDATE = 'IOEVENT:ASSETS:UPDATED:lwzAwwnpz:'
  REMOVE = 'IOEVENT:ASSETS:REMOVED:d3Gcrbv9ezTf7dyb7:'
  # IOEVENT_PEOPLE_GROUP_TEAM_CONFIGURED_prefix = 'IOEVENT_PEOPLE_GROUP_TEAM_CONFIGURED:ZNvAgNYKcEG5TNI:'
  # IOEVENT_PEOPLE_GROUP_TEAM_REMOVED           = 'IOEVENT_PEOPLE_GROUP_TEAM_REMOVED:7xWnQnU:'
  # IOEVENT_SITE_GROUPS_CONFIGRED_prefix        = 'IOEVENT_SITE_GROUPS_CONFIGRED:dx8XECJUjkGwkA:'
  IOEVENT_ASSETS_CONFIGRED_prefix = 'IOEVENT_ASSETS_CONFIGRED:B11XCb8hAP5:'
  # IOEVENT_ASSETS_FORMS_SUBMISSION_prefix      = 'IOEVENT_ASSETS_FORMS_SUBMISSION:kLctvwLigtUAaHzTD:'


class Assets(MixinTimestamps, MixinIncludesTags, MixinByIds, MixinByIdsAndType, MixinExistsID, MixinFieldMergeable, _dbcli.Model):
  __tablename__ = assetsTable

  # ID
  id: Mapped[int] = mapped_column(primary_key = True)

  # fields
  # Descriptive name for the asset (e.g., "Laptop", "Office Space")
  name: Mapped[str]
  # Identifier.unique for an asset
  code: Mapped[Optional[str]] = mapped_column(unique = True)
  # search key:unique
  key: Mapped[Optional[str]] = mapped_column(default = uuid)
  # The category of the asset (e.g., "Physical", "Digital", "Financial")
  type: Mapped[Optional[str]]
  # Physical or digital location of the asset (e.g., "Warehouse 1", "Cloud Server")
  location: Mapped[Optional[str]]
  # Indicates the current status (e.g., "Active", "Disposed", "Maintenance", "Sold")
  status: Mapped[Optional[str]]
  # Condition of the asset (e.g., "New", "Good", "Needs Repair")
  condition: Mapped[Optional[str]]
  # Detailed description of the asset
  notes: Mapped[Optional[str]]
  # additional data
  data: Mapped[Optional[dict]] = mapped_column(JSON)

  # virtual
  #  Additional tags or keywords related to the asset for easier categorization or searchability
  tags: Mapped[List['Tags']] = relationship(secondary = ln_assets_tags, back_populates = 'assets')
  #  addtional related records
  docs: Mapped[List['Docs']] = relationship(back_populates = 'asset')
  #  related site orders
  site_orders: Mapped[List['Orders']] = relationship(back_populates = 'site')
  # related assetSites:orders
  orders: Mapped[List['Orders']] = relationship(secondary = ln_orders_products, back_populates = 'products')

  # self-referential, has|belongs-to assets
  assets_has: Mapped[List['Assets']] = relationship(
    secondary     = ln_assets_assets, 
    primaryjoin   = id == ln_assets_assets.c.asset_l_id, 
    secondaryjoin = id == ln_assets_assets.c.asset_r_id, 
    backref       = backref('assets_belong', lazy = 'dynamic'),
    # back_populates = 'assets'
  )

  
  # public
  def tags_add(self, *tags, _commit = True):
    changes = 0

    for tname in filter(lambda p: not self.includes_tags(p), tags):
      tp = Tags.by_name(tname, create = True, _commit = _commit)
      tp.assets.append(self)
      changes += 1
    
    if (0 < changes) and (True == _commit):
      _dbcli.session.commit()
    
    return changes


  # public
  def tags_rm(self, *tags, _commit = True):
    changes = 0

    for tname in filter(lambda p: self.includes_tags(p), tags):
      tp = Tags.by_name(tname, create = True, _commit = _commit)
      tp.assets.remove(self)
      changes += 1
    
    if (0 < changes) and (True == _commit):
      _dbcli.session.commit()
    
    return changes
  

  # public
  def is_status(self, s):
    return s == self.status


  # public
  def is_status_active(self):
    return self.is_status(AssetsStatus.ACTIVE.value)
    

  # public
  def serialize_to_text_search(self):
    return ' '.join(v for v in SchemaSerializeAssetsTextSearch().dump(self).values() if v).lower()
  

  # public
  #  join parent assets
  def assets_join(self, *lsa):
    changes = 0
    for a in filter(lambda a_: a_ not in self.assets_belong, lsa):
      self.assets_belong.append(a)
      changes += 1

    return changes
  
  
  # public
  #  leave parent assets
  def assets_leave(self, *lsa):
    changes = 0
    for a in filter(lambda a_: a_ in self.assets_belong, lsa):
      self.assets_belong.remove(a)
      changes += 1

    return changes
    
  
  # public
  def category_key(self):
    return _dbcli.session.scalar(
      _dbcli.select(
        Tags.tag
      ).join(
        Assets.tags
      ).where(
        Assets.id == self.id,
        Tags.tag.startswith(Config.CATEGORY_KEY_ASSETS_prefix)
      ))


  # public
  def category_key_commit(self, c_key, *, _commit = True):
    _res = False
    if c_key:
      c_tag = f'{Config.CATEGORY_KEY_ASSETS_prefix}{c_key}'
      if c_tag != self.category_key():
        self.category_key_drop(_commit = _commit)
        c = Tags.by_name(c_tag, create = True, _commit = _commit)
        c.assets.append(self)
        
        if _commit:
          _dbcli.session.commit()
        
        _res = True
    
    return _res
  

  # public
  def category_key_drop(self, *, _commit = True):
    changes = 0

    for ct in filter(lambda t: t.tag.startswith(Config.CATEGORY_KEY_ASSETS_prefix), self.tags):
      ct.assets.remove(self)
      changes += 1
    
    if 0 < changes:
      if _commit:
        _dbcli.session.commit()

    return changes
  

  # public
  def get_data(self):
    d = self.data if None != self.data else {}
    return d.copy()
  

  @staticmethod
  def assets_parents(*lsa, PtAIDS = None, TYPE = None, DISTINCT = True):
    '''
      list provided node's parent assets; that contain provided nodes;
      example: 
        find stores containing product, 
        for account's groups related parent assets:sites,
      @PtAIDS; only provided parent assets IDs
    '''
    aids = map(lambda a: a.id, lsa)
    AssetsAliasedParent = aliased(Assets)
    q = _dbcli.select(
      AssetsAliasedParent.id
    ).join(
      ln_assets_assets,
      ln_assets_assets.c.asset_l_id == AssetsAliasedParent.id
    ).join(
      Assets,
      ln_assets_assets.c.asset_r_id == Assets.id
    ).where(
      Assets.id.in_(aids))

    if TYPE:
      q = q.where(
        TYPE == AssetsAliasedParent.type)
    
    if PtAIDS:
      q = q.where(
        AssetsAliasedParent.id.in_(PtAIDS))
    
    if DISTINCT:
      q = q.distinct()

    return _dbcli.session.scalars(
      _dbcli.select(
        Assets
      ).where(
        Assets.id.in_(q)))


  @staticmethod
  def assets_children(*lsa, TYPE = None, DISTINCT = True):
    '''
      list provided node's child assets; that belong to provided nodes
      example: 
        find products from stores,
    '''
    aids = map(lambda a: a.id, lsa)
    AssetsAliasedParrent = aliased(Assets)
    q = _dbcli.select(
      Assets.id
    ).join(
      ln_assets_assets,
      ln_assets_assets.c.asset_r_id == Assets.id
    ).join(
      AssetsAliasedParrent,
      ln_assets_assets.c.asset_l_id == AssetsAliasedParrent.id
    ).where(
      AssetsAliasedParrent.id.in_(aids))
    
    if None != TYPE:
      q = q.where(
        TYPE == Assets.type)
    
    if DISTINCT:
      q = q.distinct()
    
    return _dbcli.session.scalars(
      _dbcli.select(
        Assets
      ).where(
        Assets.id.in_(q)))

  
  @staticmethod
  def codegen(*, length = 10, prefix = 'Assets:'):
    return f'{prefix}{Unique.id(length = length)}'

  
  @staticmethod
  def products_all():
    return _dbcli.session.scalars(
      _dbcli.select(
        Assets
      ).where(
        AssetsType.PHYSICAL_PRODUCT.value == Assets.type,
      ))
  

  @staticmethod
  def products_only(*pids):
    '''
      list products by provided ids
    '''
    return _dbcli.session.scalars(
      _dbcli.select(
        Assets
      ).where(
        AssetsType.PHYSICAL_PRODUCT.value == Assets.type,
        Assets.id.in_(pids),
      ))

  
  @staticmethod
  def stores_all():
    return _dbcli.session.scalars(
      _dbcli.select(
        Assets
      ).where(
        AssetsType.PHYSICAL_STORE.value == Assets.type,
      ))

  
  @staticmethod
  def stores_only(*sids):
    '''
      list products by provided ids
    '''
    return _dbcli.session.scalars(
      _dbcli.select(
        Assets
      ).where(
        AssetsType.PHYSICAL_STORE.value == Assets.type,
        Assets.id.in_(sids),
      ))


# bind listener for Assets:group .location 
#  update lat:lng @data.coords if location provided
# @event.listens_for(Assets.location, 'set')
# def on_updated_assets_sites_location(asset, value, _oldvalue, _initiator):
#   changes = 0
#   if (AssetsType.PEOPLE_GROUP_TEAM.value == asset.type):
#     if not value:
#       # @empty, clear current lat:lng
#       asset.data_update(
#         patch = {
#           'coords': None
#         })
#       changes += 1

#     else:
#       from servcies.googlemaps import geocode_address
#       res = geocode_address(value)
#       asset.data_update(
#         patch = {
#           'coords': None if res['error'] else res['status']['coords']})
#       changes += 1
    
#     if 0 < changes:
#       _dbcli.session.commit()
  

##
## assets table fields @chatGPT response
##

# When designing a database table for managing general company assets, you'll want to include fields that capture essential details about each asset. Here’s a basic outline of fields you might include:

# AssetID (Primary Key): A unique identifier for each asset.
# AssetName: The name or description of the asset.
# Category: The category or type of asset (e.g., IT equipment, furniture, vehicles).
# Location: The physical location or department where the asset is stored.
# PurchaseDate: The date the asset was acquired.
# PurchasePrice: The cost of acquiring the asset.
# CurrentValue: The current value of the asset (may be updated periodically).
# Condition: The current condition of the asset (e.g., New, Good, Needs Repair).
# SerialNumber: A unique serial number or identification number assigned to the asset.
# WarrantyExpiration: The expiration date of the asset’s warranty, if applicable.
# LastServiceDate: The date of the last maintenance or service performed on the asset.
# AssignedTo: The person or department to which the asset is assigned.
# Status: The current status of the asset (e.g., In Use, In Storage, Disposed).
# Notes: Any additional notes or comments about the asset.

# google_calendar :config
#  .data.shareable_link
#  .data.public_url

