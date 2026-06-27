# Repository Usage Guide

## 1. Create Session

```python
from database.session import SessionLocal

session = SessionLocal()
```

---

## 2. Create Repository

```python
from repositories import BookRepository

book_repo = BookRepository(session)
```

---

## 3. Create Object

```python
book = Book(...)

book_repo.create(book)

session.commit()
```

---

## 4. Get By ID

```python
book = book_repo.get_by_id(book_id)
```

Returns:

- `Book` if found.
- `None` if not found.

---

## 5. Get All

```python
books = book_repo.get_all()
```

Returns a list of all records.

---

## 6. Check Exists

```python
exists = book_repo.exists(book_id)
```

Returns `True` or `False`.

---

## 7. Count Records

```python
total = book_repo.count()
```

Returns total number of records.

---

## 8. Delete

```python
book_repo.delete(book)

session.commit()
```

---

## 9. Custom Queries

Example:

```python
book_repo.search("Python")

book_repo.get_by_author("John")

book_repo.get_available_books()

registration_request_repo.get_pending_requests()
```

Each repository provides additional query methods for its own entity.

---

## 10. Transaction

After **Create**, **Update** or **Delete**, remember to commit:

```python
session.commit()
```

If an error occurs:

```python
session.rollback()
```

---

## 11. Close Session

```python
session.close()
```

or

```python
try:
    ...
finally:
    session.close()
```

---

## Notes

- Always access the database through a Repository.
- Do not write SQL directly in Service.
- One Repository manages one Entity.
- Repository only handles database operations; business logic belongs in Service.
