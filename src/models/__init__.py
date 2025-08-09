
from flask_app  import db
from src.config import Config


_err, _dbcli = db

tblSuffix_dev        = Config.TABLE_NAME_SUFFIX_dev
tblSuffix_production = Config.TABLE_NAME_SUFFIX_production

tblSuffix = tblSuffix_production if Config.PRODUCTION else tblSuffix_dev

# tables --names
tagsTable   = f'tags{tblSuffix}'
docsTable   = f'docs{tblSuffix}'
assetsTable = f'assets{tblSuffix}'
ordersTable = f'orders{tblSuffix}'

lnTableDocsTags       = f'ln_docs_tags{tblSuffix}'
lnTableAssetsTags     = f'ln_assets_tags{tblSuffix}'
lnTableAssetsAssets   = f'ln_assets_assets{tblSuffix}'
lnTableOrdersTags     = f'ln_orders_tags{tblSuffix}'
lnTableOrdersProducts = f'ln_orders_products{tblSuffix}'

# tables --ln
ln_docs_tags = _dbcli.Table(
  lnTableDocsTags,
  _dbcli.Column('doc_id', _dbcli.ForeignKey(f'{docsTable}.id'), primary_key = True),
  _dbcli.Column('tag_id', _dbcli.ForeignKey(f'{tagsTable}.id'), primary_key = True),
)

ln_assets_tags = _dbcli.Table(
  lnTableAssetsTags,
  _dbcli.Column('asset_id', _dbcli.ForeignKey(f'{assetsTable}.id'), primary_key = True),
  _dbcli.Column('tag_id',   _dbcli.ForeignKey(f'{tagsTable}.id'),   primary_key = True),
)

ln_assets_assets = _dbcli.Table(
  lnTableAssetsAssets,
  _dbcli.Column('asset_l_id', _dbcli.ForeignKey(f'{assetsTable}.id'),  primary_key = True),
  _dbcli.Column('asset_r_id', _dbcli.ForeignKey(f'{assetsTable}.id'),  primary_key = True),
)

ln_orders_tags = _dbcli.Table(
  lnTableOrdersTags,
  _dbcli.Column('order_id', _dbcli.ForeignKey(f'{ordersTable}.id'), primary_key = True),
  _dbcli.Column('tag_id',   _dbcli.ForeignKey(f'{tagsTable}.id'),   primary_key = True),
)

ln_orders_products = _dbcli.Table(
  lnTableOrdersProducts,
  _dbcli.Column('order_id',   _dbcli.ForeignKey(f'{ordersTable}.id'), primary_key = True),
  _dbcli.Column('product_id', _dbcli.ForeignKey(f'{assetsTable}.id'), primary_key = True),
  _dbcli.Column('amount', _dbcli.Integer, nullable = False, default = 0),
)

