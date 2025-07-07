# Delete existing migrations and regenerate them to fix circular dependency

# The following commands need to be run:
# 1. Delete migration files (but keep __init__.py)
# 2. Run makemigrations
# 3. Run migrate

echo "Cleaning up existing migrations..."
find /Users/happyfox/Documents/HappyFox/Zeroqueue -name "0001_initial.py" -path "*/migrations/*" -delete
echo "Migrations cleaned. Now run:"
echo "python manage.py makemigrations"
echo "python manage.py migrate"