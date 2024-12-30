class User(AbstractBaseUser):
    """Custom User model with HMAC + Salt for password handling."""
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=100, blank=True, null=True)  # Token for password reset
    password_history = models.JSONField(default=list)  # Field for storing password history
    failed_login_attempts = models.IntegerField(default=0)  # Tracking failed login attempts
    last_failed_login = models.DateTimeField(null=True, blank=True)  # Time of last failed login

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def set_password(self, raw_password):
        """Override set_password to use HMAC + Salt and update password history."""
        if raw_password:
            self.validate_password_strength(raw_password)

            salt = os.urandom(16).hex()  # Generate a random Salt
            hashed_password = hmac.new(salt.encode(), raw_password.encode(), hashlib.sha256).hexdigest()
            new_password = f'{salt}${hashed_password}'  # Save salt and hash in the format: salt$hashed_password
            
            # Check if the new password matches the recent password history
            if any(hmac.compare_digest(old.split('$')[1], hashed_password) for old in self.password_history[-config["password_history"]:]): 
                raise ValueError("Password cannot match the last 3 passwords.")
            
            # Update password and history
            self.password = new_password
            self.password_history.append(new_password)
            self.password_history = self.password_history[-config["password_history"]:]

    def check_password(self, raw_password):
        """Verify the user's password."""
        if not self.password:
            return False
        try:
            salt, stored_hash = self.password.split('$')
            entered_hash = hmac.new(salt.encode(), raw_password.encode(), hashlib.sha256).hexdigest()
            return stored_hash == entered_hash
        except ValueError:
            return False

    def validate_password_strength(self, password):
        """Ensure password meets all strength requirements."""
        if len(password) < config["min_password_length"]:
            raise ValidationError(f"Password must be at least {config['min_password_length']} characters long.")
        
        if config["password_requirements"]["uppercase"] and not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        if config["password_requirements"]["lowercase"] and not any(c.islower() for c in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        if config["password_requirements"]["digits"] and not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one digit.")
        
        if config["password_requirements"]["special_characters"] and not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
            raise ValidationError("Password must contain at least one special character.")

        if config["dictionary_check"]:
            common_passwords = ["123456", "password", "qwerty"]  # Example list
            if password in common_passwords:
                raise ValidationError("Password cannot be a common password.")
        
    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        """Check if the user has admin privileges."""
        return self.is_admin
