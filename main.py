# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Cho phép frontend HTML/CSS/JS gọi API này
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# books = [
#     {
#         "id": 1,
#         "title": "Python Cơ Bản",
#         "author": "Nguyễn Văn A",
#         "category": "Programming",
#         "description": "Sách học Python cơ bản cho người mới bắt đầu",
#         "status": "available",
#     },
#     {
#         "id": 2,
#         "title": "Java Cơ Bản",
#         "author": "Trần Văn B",
#         "category": "Programming",
#         "description": "Sách học Java cơ bản",
#         "status": "borrowed",
#     },
#     {
#         "id": 3,
#         "title": "HTML CSS",
#         "author": "Lê Văn C",
#         "category": "Web",
#         "description": "Sách học thiết kế giao diện web",
#         "status": "available",
#     },
# ]


# @app.get("/")
# def home():
#     return {"message": "Library Management API is running"}


# @app.get("/books")
# def get_books():
#     return books


# @app.get("/books/search/")
# def search_books(keyword: str = ""):
#     result = []
#     keyword_lower = keyword.lower()

#     for book in books:
#         if (
#             keyword_lower in book["title"].lower()
#             or keyword_lower in book["author"].lower()
#             or keyword_lower in book["category"].lower()
#         ):
#             result.append(book)

#     return result


# @app.get("/books/{book_id}")
# def get_book_by_id(book_id: int):
#     for book in books:
#         if book["id"] == book_id:
#             return book

#     return {"message": "Book not found"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from api.registration_api import router as registration_router
from api.auth_api import router as auth_router
from api.book_api import router as book_router
from api.report_api import router as report_router
from api.librarian_api import router as librarian_router
from api.borrowRecord_api import router as borrow_record_router
from api.reader_api import router as reader_router
from api.category_api import router as category_router
from api.reader_management_api import router as reader_management_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

# HTML
templates = Jinja2Templates(directory="frontend")

# API
app.include_router(registration_router)
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(report_router)
app.include_router(librarian_router)
app.include_router(borrow_record_router)
app.include_router(reader_router)
app.include_router(category_router)
app.include_router(reader_management_router)



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request
        }
    )
