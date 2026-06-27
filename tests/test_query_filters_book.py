from database.session import SessionLocal
from repositories import BookRepository

def test_filters_books():

    session = SessionLocal()
    repo = BookRepository(session)

    # print("\n=== Get by title ===")

    # results = repo.get_by_title("Python")

    # print(f"Found: {len(results)}")

    # for book in results:
    #     print(book.title)

    print("\n=== Search ===")

    results = repo.search("John")

    print(f"Found: {len(results)}")

    for book in results:
        print(book.title)


if __name__ == "__main__":

    test_filters_books()