
from datetime import datetime
from datetime import timezone

def utcnow():
  return datetime.now(tz = timezone.utc)

def with_doc_timestamps(doc, *, 
    field_created_at = 'created_at', 
    field_updated_at = 'updated_at'):
  tt = utcnow()
  doc.setdefault(field_created_at, tt)
  doc[field_updated_at] = tt
  return doc

