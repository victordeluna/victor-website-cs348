from flask import Flask, render_template, request, jsonify
from database import upload_book, erase_book, update_book, get_books

app = Flask(__name__) 

@app.route("/")

def hello_world():
  return render_template ("index.html")
  
@app.route("/add")

def add():
  return render_template ("add.html")



@app.route("/add_book", methods=['POST'])

def add_book():
  title = request.form['title']
  author = request.form['author']
  library = request.form['library']
  num_pages = request.form['num_pages']
  genre = request.form['genre']
  taken = request.form['taken']
  release_date = request.form['release_date']
  
  try:
    upload_book(title, author, library, num_pages, genre, taken, release_date)
    return jsonify(success=True, message='Book added successfully!!')
  except Exception as e:
    return jsonify(success=False, message=str(e))


@app.route("/delete_book", methods=['POST'])

def delete_book():
    title = request.form['title']
    author = request.form['author']
    library = request.form['library']

    try:
      erase_book(title, author, library)
      return jsonify(success=True, message='Book deleted successfully!!')
    except Exception as e:
      return jsonify(success=False, message=str(e))


@app.route("/edit_book", methods=['POST'])

def edit_book():
  title = request.form['title']
  author = request.form['author']
  library = request.form['library']
  num_pages = request.form['num_pages']
  genre = request.form['genre']
  taken = request.form['taken']
  release_date = request.form['release_date']

  try:
    update_book(title, author, library, num_pages, genre, taken, release_date)
    return jsonify(success=True, message='Book edited successfully!!')
  except Exception as e:
    return jsonify(success=False, message=str(e))


@app.route("/display_books", methods=['POST'])
def display_books():
  author = request.form['author']
  library = request.form['library']
  book_info = get_books(author, library)

  # Assuming you have a display.html template where you want to show the results
  return render_template("display.html", book_info=book_info)


@app.route("/delete")

def delete():
  return render_template ("delete.html")

@app.route("/edit")

def edit():
  return render_template ("edit.html")

@app.route("/display")

def display():
  return render_template ("display.html")

if __name__ == '__main__':        
  app.run(host='0.0.0.0', debug=True)

