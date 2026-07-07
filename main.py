from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cho phép frontend HTML/CSS/JS gọi API này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

books = [
    {
        "id": 1,
        "title": "Python Cơ Bản",
        "author": "Nguyễn Văn A",
        "category": "Programming",
        "description": "Sách học Python cơ bản cho người mới bắt đầu",
        "status": "available",
    },
    {
        "id": 2,
        "title": "Java Cơ Bản",
        "author": "Trần Văn B",
        "category": "Programming",
        "description": "Sách học Java cơ bản",
        "status": "borrowed",
    },
    {
        "id": 3,
        "title": "HTML CSS",
        "author": "Lê Văn C",
        "category": "Web",
        "description": "Sách học thiết kế giao diện web",
        "status": "available",
    },
]


@app.get("/")
def home():
    return {"message": "Library Management API is running"}


@app.get("/books")
def get_books():
    return books


@app.get("/books/search/")
def search_books(keyword: str = ""):
    result = []
    keyword_lower = keyword.lower()

    for book in books:
        if (
            keyword_lower in book["title"].lower()
            or keyword_lower in book["author"].lower()
            or keyword_lower in book["category"].lower()
        ):
            result.append(book)

    return result


@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    return {"message": "Book not found"}