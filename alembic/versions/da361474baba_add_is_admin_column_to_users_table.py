"""Add is_admin column to users table

Revision ID: da361474baba
Revises: 
Create Date: 2024-11-19 09:17:43.290898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da361474baba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'is_admin' column to the users table
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))

    # Workaround for unsupported operations in SQLite:
    # Recreate affected tables where necessary changes are required.

    # Recreate 'audit_logs' table with updated 'user_id' column
    op.create_table(
    'audit_logs_temp',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('action', sa.String(100), nullable=False),
    sa.Column('timestamp', sa.DateTime, nullable=True),  # Example additional column
)
# Copy data back to the original 'audit_logs' schema
    op.execute('INSERT INTO audit_logs_temp (id, user_id, action, timestamp) SELECT id, user_id, action, timestamp FROM audit_logs')
    op.drop_table('audit_logs')
    op.rename_table('audit_logs_temp', 'audit_logs')

    # Recreate 'order_items' table with nullable columns
    op.create_table(
        'order_items_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, nullable=True),
        sa.Column('product_id', sa.Integer, nullable=True),
        sa.Column('quantity', sa.Integer, nullable=True),
        sa.Column('price_at_purchase', sa.Float, nullable=True),
    )
    op.execute('INSERT INTO order_items_temp SELECT * FROM order_items')
    op.drop_table('order_items')
    op.rename_table('order_items_temp', 'order_items')

    # Recreate 'products' table without dropped columns
    op.create_table(
        'products_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=True),
    )
    op.execute('INSERT INTO products_temp (id, name) SELECT id, name FROM products')
    op.drop_table('products')
    op.rename_table('products_temp', 'products')

    # Recreate 'reviews' table with updated columns
    op.create_table(
        'reviews_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, nullable=True),
        sa.Column('rating', sa.Float, nullable=True),
    )
    op.execute('INSERT INTO reviews_temp SELECT id, product_id, rating FROM reviews')
    op.drop_table('reviews')
    op.rename_table('reviews_temp', 'reviews')

    # Drop 'carts' table
    op.drop_table('carts')

    # Drop columns in 'orders' table
    op.create_table(
        'orders_temp',
        sa.Column('id', sa.Integer, primary_key=True),
    )
    op.execute('INSERT INTO orders_temp (id) SELECT id FROM orders')
    op.drop_table('orders')
    op.rename_table('orders_temp', 'orders')


def downgrade():
    # Reverse the 'is_admin' addition
    op.drop_column('users', 'is_admin')

    # Revert 'audit_logs'
    op.create_table(
        'audit_logs_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('action', sa.String(100), nullable=False),
    )
    op.execute('INSERT INTO audit_logs_temp SELECT * FROM audit_logs')
    op.drop_table('audit_logs')
    op.rename_table('audit_logs_temp', 'audit_logs')

    # Revert 'order_items'
    op.create_table(
        'order_items_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, nullable=False),
        sa.Column('product_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('price_at_purchase', sa.Float, nullable=False),
    )
    op.execute('INSERT INTO order_items_temp SELECT * FROM order_items')
    op.drop_table('order_items')
    op.rename_table('order_items_temp', 'order_items')

    # Revert 'products'
    op.create_table(
        'products_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('stock', sa.Integer, nullable=False),
        sa.Column('rating', sa.Float, nullable=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('description', sa.String(500), nullable=True),
    )
    op.execute('INSERT INTO products_temp SELECT * FROM products')
    op.drop_table('products')
    op.rename_table('products_temp', 'products')

    # Revert 'reviews'
    op.create_table(
        'reviews_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, nullable=False),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('comment', sa.String(500), nullable=True),
        sa.Column('review_date', sa.DateTime, nullable=True),
    )
    op.execute('INSERT INTO reviews_temp SELECT * FROM reviews')
    op.drop_table('reviews')
    op.rename_table('reviews_temp', 'reviews')

    # Recreate 'carts'
    op.create_table(
        'carts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('product_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
    )

    # Restore 'orders'
    op.create_table(
        'orders_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('total_amount', sa.Float, nullable=False),
    )
    op.execute('INSERT INTO orders_temp SELECT * FROM orders')
    op.drop_table('orders')
    op.rename_table('orders_temp', 'orders')