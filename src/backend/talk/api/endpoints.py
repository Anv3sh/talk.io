from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from talk.api.auth import (
    authenticate_user,
    create_user_tokens,
    get_current_user,
    get_password_hash,
)
from talk.api.schema import LoginResponseSchema, UserAuth
from talk.services.chat.manager import ConnectionManager
from talk.services.database.connections import get_db_session
from talk.services.database.models.user import User
from talk.services.database.operations.user import get_user_by_email

user_router = APIRouter(prefix="/user", tags=["User"])
chat_router = APIRouter(prefix="/ws", tags=["Chat"])


chat_manager = ConnectionManager()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8080/talk/api/ws/%s");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


# User authentication and authorization
@user_router.post(
    "/signup", summary="User registration", status_code=status.HTTP_201_CREATED
)  # noqa
async def signup(data: UserAuth, session: Session = Depends(get_db_session)):  # noqa
    """
    User registration
    """
    user = get_user_by_email(db=session, email=data.email)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist.",
        )

    user_map = {
        "email": data.email,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "password": get_password_hash(data.password),
        "user_id": str(uuid4()),
    }
    user_model = User(**user_map)

    session.add(user_model)
    session.commit()

    return {
        "details": "Signup successful",  # noqa
    }


@user_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=LoginResponseSchema,
)  # noqa
async def login_to_get_tokens(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    if user := authenticate_user(form_data.username, form_data.password, db):
        tokens = create_user_tokens(
            user_id=user.user_id, db=db, update_last_login=True
        )  # noqa
        return {"user": user, **tokens}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.get(
    "/health",
    summary="Health check",
    status_code=status.HTTP_200_OK,
)
async def health(user: User = Depends(get_current_user)):
    return {
        "status": 200,
        "body": {"message": "Health ok!"},
    }


@user_router.get("/{client_id}")
async def get(client_id: int):
    return HTMLResponse(html % (client_id))


@chat_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.send_personal_message(f"You wrote: {data}", websocket)
            await chat_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
        await chat_manager.broadcast(f"Client #{client_id} left the chat")
