from django.db import models

# Create your models here.
class AdminUser(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateField()
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title
    
class Account(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='accounts')

    def __str__(self):
        return self.username

class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    dob = models.DateField()
    score = models.IntegerField(default=0)
    preferences = models.TextField(blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.name

class Expert(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    field_of_expertise = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Consultation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='consultations')
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f'Consultation on {self.date}'

class Test(models.Model):
    test_name = models.CharField(max_length=200)
    test_type = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.test_name

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Result for {self.user.name} - {self.score}'

class Forum(models.Model):
    topic = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forums')

    def __str__(self):
        return self.topic

class AIChatbot(models.Model):
    question = models.TextField()
    response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatbots')

    def __str__(self):
        return self.question
