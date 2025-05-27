import unittest
from sqlalchemy.orm import Session
from app.models import Post
from app.schemas import PostCreate
from routers.posts import create_post, read_post, update_post, delete_post, search_posts
from app.database import SessionLocal

class TestPosts(unittest.TestCase):
    def setUp(self):
        """
        Set up a database session for testing.
        """
        self.db: Session = SessionLocal()

    def tearDown(self):
        """
        Close the database session after each test.
        """
        self.db.close()

    def test_create_post(self):
        post_data = PostCreate(title="Test Post", content="This is a test post.")
        response = create_post(user_id=1, post=post_data, db=self.db)
        self.assertEqual(response.title, post_data.title)
        self.assertEqual(response.content, post_data.content)

    def test_read_post(self):
        post = self.db.query(Post).first()
        response = read_post(post_id=post.id, db=self.db)
        self.assertEqual(response.id, post.id)
        self.assertEqual(response.title, post.title)

    def test_update_post(self):
        post = self.db.query(Post).first()
        updated_data = PostCreate(title="Updated Title", content="Updated content.")
        response = update_post(post_id=post.id, post=updated_data, db=self.db)
        self.assertEqual(response.title, updated_data.title)
        self.assertEqual(response.content, updated_data.content)

    def test_delete_post(self):
        post = self.db.query(Post).first()
        response = delete_post(post_id=post.id, db=self.db)
        self.assertEqual(response.id, post.id)
        self.assertIsNone(self.db.query(Post).filter(Post.id == post.id).first())

    def test_search_posts(self):
        search_query = "Test"
        response = search_posts(query=search_query, db=self.db)
        self.assertGreater(len(response), 0)
        for post in response:
            self.assertTrue(search_query in post.title or search_query in post.content)

if __name__ == "__main__":
    unittest.main()