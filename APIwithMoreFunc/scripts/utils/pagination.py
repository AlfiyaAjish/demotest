def paginate(data, page: int, limit: int):
    total = len(data)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    return {
        "total": total,
        "limit": limit,
        "page": page,
        "total_pages": total_pages,
        "data": data[start:end]
    }
