from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        # ตรวจสอบความถูกต้องของอีเมลและชื่อผู้ใช้
        if not email:
            raise ValueError('ผู้ใช้ต้องมีที่อยู่อีเมล')
        if not username:
            raise ValueError('ผู้ใช้ต้องมีชื่อผู้ใช้')

        # สร้างอินสแตนซ์ของโมเดลผู้ใช้
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        # ตั้งค่ารหัสผ่านและบันทึกผู้ใช้
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        # สร้างผู้ใช้ที่มีสิทธิ์ของผู้ดูแลระบบ
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # ตั้งค่าแอตทริบิวต์ของผู้ดูแลระบบและบันทึก
        user.admin = True
        user.is_active = True
        user.staff = True
        user.superadmin = True
        user.save(using=self._db)
        return user
    
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True) # เพิ่มแอตทริบิวต์ phone_number ที่นี่

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    # ตรวจสอบว่าผู้ใช้มีสิทธิ์เฉพาะหรือไม่
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # ตรวจสอบว่าผู้ใช้มีสิทธิ์ในโมดูลหรือไม่
    def has_module_perms(self, add_label):
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member"
        return self.admin
    
    @property
    def is_superadmin(self):
        "Is the user a super admin member"
        return self.superadmin

