import unittest
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

class TestComments(unittest.TestCase):
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

    def test_create_comment(self):
        # Create a user
        user = models.User(username="testuser", email="test@example.com", password="hashedpassword")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # Create a post
        post = models.Post(title="Test Post", content="This is a test post.", owner_id=user.id)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        # Create a comment
        comment_data = schemas.CommentCreate(content="This is a test comment.")
        comment = models.Comment(content=comment_data.content, post_id=post.id, author_id=user.id)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        self.assertEqual(comment.content, comment_data.content)
        self.assertEqual(comment.post_id, post.id)
        self.assertEqual(comment.author_id, user.id)

    def test_get_comments(self):
        # Assuming a comment already exists
        comment = self.db.query(models.Comment).first()
        self.assertIsNotNone(comment)

        # Retrieve comments for a specific post
        comments = self.db.query(models.Comment).filter(models.Comment.post_id == comment.post_id).all()
        self.assertGreater(len(comments), 0)

    def test_delete_comment(self):
        # Create a user and a post
        user = models.User(username="testuser", email="test@example.com", password="hashedpassword")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        post = models.Post(title="Test Post", content="This is a test post.", owner_id=user.id)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        # Create a comment
        comment = models.Comment(content="This is a test comment.", post_id=post.id, author_id=user.id)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        # Delete the comment
        self.db.delete(comment)
        self.db.commit()

        # Verify the comment is deleted
        deleted_comment = self.db.query(models.Comment).filter(models.Comment.id == comment.id).first()
        self.assertIsNone(deleted_comment)

if __name__ == "__main__":
    unittest.main()