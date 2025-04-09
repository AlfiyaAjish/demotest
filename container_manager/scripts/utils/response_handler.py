from fastapi import HTTPException

def handle_exception(e: Exception, message="Internal server error", status_code=500):
    raise HTTPException(status_code=status_code, detail=f"{message}: {str(e)}")
