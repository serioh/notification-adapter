import os
from typing import Optional

import uvicorn
from fastapi import Request, Header, FastAPI, Query, Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from email_service import authenticate, send_message, create_message
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-KEY"

api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


@app.post("/send-email", status_code=201)
async def read_html(body: Request,
                    api_key_header: str = Security(api_key_header_auth),
                    subject_line: str = Header(None),
                    recipients: Optional[list[str]] = Query(None)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    request_bytes = await body.body()
    html_message = request_bytes.decode("UTF-8")
    service = authenticate()
    response = send_message(service, 'me', create_message('me', recipients, subject_line, html_message))
    return {
        "response": response
    }


if __name__ == "__main__":
    uvicorn.run("gmail.api:app", reload=True)
