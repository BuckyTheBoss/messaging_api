from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
	subject = models.TextField()
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
	is_read = models.BooleanField(default=False)

	def __str__(self):
		return f'Message from: {self.sender.username} to {self.receiver.username}'
