import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine(
    "mysql+pymysql://victordelunap:G9WWXqUuFS8FlPGA4Pmg@cs348db.cpg8a8mounod.us-east-2.rds.amazonaws.com:3306/cs348db?charset=utf8mb4"
)

Session = sessionmaker(bind=engine)


def upload_book(title, author, library, num_pages, genre, taken, release_date):
  with Session.begin() as session:
      try:
          session.execute(
              text(
                  "INSERT INTO Book (title, author, library, num_pages, genre, taken, release_date) VALUES (:title, :author, :library, :num_pages, :genre, :taken, :release_date)"
              ),
              {
                  "title": title,
                  "author": author,
                  "library": library,
                  "num_pages": num_pages,
                  "genre": genre,
                  "taken": taken,
                  "release_date": release_date
              }
          )

          num_books = get_num_books(library)

          session.execute(
              text(
                  "UPDATE Library SET num_books= :num_books WHERE libname = :library"
              ),
              {
                  "num_books": num_books + 1,
                  "library": library
              }
          )


          session.execute(
              text(
                  "UPDATE Library AS l SET l.num_genres = (SELECT COUNT(DISTINCT genre) FROM Book AS b WHERE b.library = l.libname) WHERE l.libname = :library"
              ),
              {
                  "library": library
              }
          )

          session.commit()
      except Exception as e:
          session.rollback()
          print(f"Error uploading book: {e}")



def erase_book(title, author, library):
  with Session.begin() as session:
    session.execute(
        text(
            "DELETE FROM Book WHERE title = :title AND author = :author AND library = :library"
        ), {
            "title": title,
            "author": author,
            "library": library
        })

    num_books = get_num_books(library)

    session.execute(
        text(
            "UPDATE Library SET num_books= :num_books WHERE libname = :library"
        ),
        {
            "num_books": num_books - 1,
            "library": library
        }
    )

    session.execute(
        text(
            "UPDATE Library AS l SET l.num_genres = (SELECT COUNT(DISTINCT genre) FROM Book AS b WHERE b.library = l.libname) WHERE l.libname = :library"
        ),
        {
            "library": library
        }
    )

    session.commit()


def update_book(title, author, library, num_pages, genre, taken, release_date):
  with Session.begin() as session:
      # Prepare the SQL UPDATE statement
      update_statement = "UPDATE Book SET "
      update_fields = []

      if author:
          update_fields.append(f"author = :author")
      if num_pages:
          update_fields.append(f"num_pages = :num_pages")
      if genre:
          update_fields.append(f"genre = :genre")
      if taken is not None and taken.isdigit():
          update_fields.append(f"taken = :taken")
      if release_date:
          update_fields.append(f"release_date = :release_date")

      update_statement += ", ".join(update_fields)
      update_statement += " WHERE title = :title AND library = :library"

      # Execute the SQL statement with provided parameters
      session.execute(
          text(update_statement),
          {
              "title": title,
              "library": library,
              "author": author,
              "num_pages": num_pages,
              "genre": genre,
              "taken": taken,
              "release_date": release_date
          }
      )

      session.commit()


def get_books(author, library):
  with Session.begin() as session:
      books_query = text("""
          SELECT title, num_pages, release_date FROM Book 
          WHERE author = :author AND library = :library
      """)

      result = session.execute(books_query, {"author": author, "library": library}).fetchall()
      books = [{"title": row[0], "num_pages": row[1], "release_date": row[2]} for row in result]
      return books


def get_num_books(library):
  with Session.begin() as session:
      num_books_query = text("""
          SELECT num_books FROM Library 
          WHERE libname = :library
      """)

      result = session.execute(num_books_query, {"library": library}).fetchone()
      if result:
          return result[0]  # Return the value of the num_books column
      else:
          return None  # Or handle the case when no result is found
