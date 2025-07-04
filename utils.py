"""Utils for the HR service"""

import re
import unicodedata

from models import ColumnConfig, Employee


def normalize(text: str) -> str:
    """Normalize text: lowercase, remove accents, trim extra spaces"""
    if not text or not text.strip():
        return None
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    return re.sub(r"\s+", " ", text).strip()


def filter_query(query, filters):
    """Filter query"""
    if filters.locations:
        locs = [normalize(loc) for loc in filters.locations]
        query = query.filter(Employee.location_search.in_(locs))

    if filters.companies:
        comps = [normalize(comp) for comp in filters.companies]
        query = query.filter(Employee.company_search.in_(comps))

    if filters.departments:
        depts = [normalize(dept) for dept in filters.departments]
        query = query.filter(Employee.department_search.in_(depts))

    if filters.positions:
        pos = [normalize(p) for p in filters.positions]
        query = query.filter(Employee.position_search.in_(pos))

    if filters.statuses:
        query = query.filter(Employee.status.in_(filters.statuses))

    return query


def get_visible_columns(db, org_id):
    """Get visible columns"""
    configs = db.query(ColumnConfig).filter_by(organization_id=org_id).all()
    return [c.column_name for c in configs]
