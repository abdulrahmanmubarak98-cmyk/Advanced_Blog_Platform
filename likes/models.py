from django.db import models
from django.contrib.auth.models import User
from account.models import Post


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_like",
            )
        ]

        def __str__(self):
            return f"{self.user.username} likes {self.post.title}"
