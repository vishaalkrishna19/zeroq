# Fix for UserAccount admin inline
# Add this line to UserAccountInline class in users/admin.py:
# fk_name = 'user'  # Specify which ForeignKey to use

# This resolves the admin.E202 error about multiple ForeignKeys to User model