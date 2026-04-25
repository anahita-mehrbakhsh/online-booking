from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('counselor', 'Counselor'),
        ('admin', 'Admin'),
        ('author', 'Author'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='counselor')
    specialties = models.CharField(max_length=255, help_text="مثلاً: خانواده، تحصیلی، شغلی")
    resume = models.TextField()
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_prerequisite = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
    )
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    prerequisite_tests = models.ManyToManyField(Test, blank=True, related_name='appointments')

    def __str__(self):
        return f"{self.client.username} - {self.counselor} - {self.start_time}"


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    answers = models.JSONField()  # برای سادگی
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    counselor = models.ForeignKey(Counselor, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user} - {self.rating}"


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percent = models.IntegerField(help_text="درصد تخفیف، مثلاً 20")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    gateway_tracking_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.created_at}"

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
