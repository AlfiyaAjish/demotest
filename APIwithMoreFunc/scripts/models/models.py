from pydantic import BaseModel, Field
from typing import Optional, Dict, Union, List
from scripts.constants.app_constants import DEFAULT_LIMIT, DEFAULT_PAGE

class QueryRequest(BaseModel):
    table: str = Field(..., description="Table name (must match allowed tables)")
    operation: str = Field(..., description="Operation type: search, filter, or sort")
    filter_input: Optional[Dict[str, Union[str, List[str]]]] = Field(default_factory=dict, description="Filter key-value pairs")
    search_input: Optional[Dict[str, Union[str, List[str]]]] = Field(default_factory=dict, description="Search key-value pairs")
    sort_input: Optional[Dict[str, str]] = Field(default_factory=dict, description="Sort field and order (asc/desc)")
    page: Optional[int] = Field(DEFAULT_PAGE, description="Pagination: page number")
    limit: Optional[int] = Field(DEFAULT_LIMIT, description="Pagination: number of items per page")


