from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class UserManager(BaseUserManager):
  
    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
       
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    name =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    address1 =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    address2 =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    avatar =  models.CharField(max_length=255,  unique=False, blank=True, null=True)
    email_verified_hash = models.CharField(max_length=50, unique=False, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email
    class Meta:
        db_table = "User"

class MusicianPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    musician = models.ForeignKey(User, on_delete=models.CASCADE, related_name='musician')
    title = models.CharField(max_length=50,  unique=False, blank=True, null=True)
    description = models.CharField(max_length=255,  unique=False, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    cagegory = models.IntegerField(blank=True, null=True)

class PostDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(MusicianPost, on_delete=models.CASCADE, related_name='musicianpost')
    availble_type = models.IntegerField(blank=True, null=True)
    deadline = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now_add=False)
    place = models.CharField(max_length=255, unique=False, blank=True, null=True)
    

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(MusicianPost, on_delete=models.CASCADE, related_name='musicianPostForOrder')
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(blank=False, default=0)
    description = models.CharField(max_length=255,  unique=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, unique=False, blank=True, null=True)
    readStatus = models.BooleanField(default=False)
    all = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

class Chatting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")
    user1 = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="user2")

class ChattingHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chattingid = models.ForeignKey(Chatting, on_delete=models.CASCADE, related_name="chatting")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senderuser")
    contents = models.CharField(max_length=1000, unique=False, blank=True, null=True)
    attach = models.CharField(max_length=255, unique=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Following(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    datetime = models.DateTimeField(auto_now_add=True)

class PaymentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="orderPayment")
    amount = models.IntegerField(default = 0)
    status = models.IntegerField(default = 0)
    datetime = models.DateTimeField(auto_now_add=True)
    widrawalDate = models.DateField(auto_now_add=False)
    expireDate = models.DateField(auto_now_add=False)

class BankDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bankOwner")
    bankName = models.CharField(max_length=50, unique=False, blank=False)
    AccountName = models.CharField(max_length=50, unique=False, blank=False)
    branchName = models.CharField(max_length=50, unique=False, blank=False)

class SystemFeeHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="orderSystemFee")
    amount = models.IntegerField(default = 0)
    fee = models.IntegerField(default = 0)
    datetime = models.DateTimeField(auto_now_add=True)