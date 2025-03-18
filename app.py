import streamlit as st
from connector import get_db_connection

st.title("📚 Personal Library Manager")


st.sidebar.header("📌 Menu")
menu_option = st.sidebar.radio("Select an Option:", ["Add Book", "View Books", "Search Book", "Mark as Read", "Statistics", "Remove Book", "Update Book", "Recommend a Book"])


def fetch_books(query="SELECT * FROM books"):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

if menu_option == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    
    if st.button("Add Book", use_container_width=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (%s, %s, %s, %s, %s)",
                       (title, author, year, genre, read))
        conn.commit()
        conn.close()
        st.success("Book added successfully!")

elif menu_option == "View Books":
    st.subheader("📚 Your Book Collection")
    books = fetch_books()
    if not books:
        st.warning("No books in the library.")
    else:
        for book in books:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - Genre: {book['genre']} - Read: {'✅' if book['read_status'] else '❌'}")

elif menu_option == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_term = st.text_input("Enter book title")
    if st.button("Search", use_container_width=True):
        books = fetch_books(f"SELECT * FROM books WHERE title LIKE '%{search_term}%'")
        if books:
            for book in books:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - Genre: {book['genre']} - Read: {'✅' if book['read_status'] else '❌'}")
        else:
            st.warning("No books found.")

elif menu_option == "Mark as Read":
    st.subheader("✔️ Mark a Book as Read")
    books = fetch_books("SELECT * FROM books WHERE read_status = 0")
    if books:
        titles = {book["title"]: book["id"] for book in books}
        selected_book = st.selectbox("Select a book to mark as read", titles.keys())
        if st.button("Mark as Read", use_container_width=True):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET read_status = 1 WHERE id = %s", (titles[selected_book],))
            conn.commit()
            conn.close()
            st.success("Book marked as read!")
    else:
        st.info("All books are already marked as read.")

elif menu_option == "Statistics":
    st.subheader("📊 Library Statistics")
    books = fetch_books()
    total_books = len(books)
    read_books = sum(1 for book in books if book["read_status"])
    unread_books = total_books - read_books
    genres = {book["genre"] for book in books}
    
    st.write(f"**Total Books:** {total_books}")
    st.write(f"✅ **Read Books:** {read_books}")
    st.write(f"❌ **Unread Books:** {unread_books}")
    st.write(f"📂 **Genres:** {', '.join(genres) if genres else 'None'}")

elif menu_option == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    books = fetch_books()
    if books:
        titles = {book["title"]: book["id"] for book in books}
        selected_book = st.selectbox("Select a book to remove", titles.keys())
        if st.button("Remove Book", use_container_width=True):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = %s", (titles[selected_book],))
            conn.commit()
            conn.close()
            st.success("Book removed successfully!")
    else:
        st.warning("No books in the library to remove.")

elif menu_option == "Update Book":
    st.subheader("✏️ Update Book Information")
    books = fetch_books()
    if books:
        titles = {book["title"]: book["id"] for book in books}
        selected_book = st.selectbox("Select a book to update", titles.keys())
        for book in books:
            if book["title"] == selected_book:
                new_title = st.text_input("New Title", book["title"])
                new_author = st.text_input("New Author", book["author"])
                new_year = st.text_input("New Publication Year", book["year"])
                new_genre = st.text_input("New Genre", book["genre"])
                new_read = st.checkbox("Read?", book["read_status"])
                if st.button("Update Book", use_container_width=True):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE books SET title=%s, author=%s, year=%s, genre=%s, read_status=%s WHERE id=%s",
                                   (new_title, new_author, new_year, new_genre, new_read, titles[selected_book]))
                    conn.commit()
                    conn.close()
                    st.success("Book updated successfully!")
    else:
        st.warning("No books available to update.")

elif menu_option == "Recommend a Book":
    st.subheader("📢 Book Recommendation")
    books = fetch_books("SELECT * FROM books WHERE read_status = 0")
    if books:
        recommended_book = books[0]
        st.write(f"📚 **{recommended_book['title']}** by {recommended_book['author']} - Genre: {recommended_book['genre']}")
    else:
        st.info("You have read all the books! Add more to get recommendations.")
