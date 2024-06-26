"""Initial migration

Revision ID: 8fe30d384ace
Revises: 
Create Date: 2023-11-11 06:39:59.049225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from utils.custom_types import EncryptedType


# revision identifiers, used by Alembic.
revision: str = '8fe30d384ace'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('mobile', sa.String(length=11), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('membership', sa.String(length=5), nullable=True),
    sa.Column('two_factor_authentication', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mobile'),
    schema='account'
    )
    op.create_index(op.f('ix_account_users_id'), 'users', ['id'], unique=False, schema='account')
    op.create_table('ufos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tax_number', EncryptedType(), nullable=True),
    sa.Column('Shaba_number', EncryptedType(), nullable=True),
    sa.Column('national_code', EncryptedType(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['account.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='account'
    )
    op.create_index(op.f('ix_account_ufos_id'), 'ufos', ['id'], unique=False, schema='account')
    op.create_table('shops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.Column('shop_name', sa.String(length=200), nullable=True),
    sa.Column('postal_code', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['account.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='shop'
    )
    op.create_index(op.f('ix_shop_shops_id'), 'shops', ['id'], unique=False, schema='shop')
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s3_key', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('link', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.shops.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['account.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='file'
    )
    op.create_index(op.f('ix_file_files_file_name'), 'files', ['file_name'], unique=False, schema='file')
    op.create_index(op.f('ix_file_files_id'), 'files', ['id'], unique=False, schema='file')
    op.create_index(op.f('ix_file_files_s3_key'), 'files', ['s3_key'], unique=True, schema='file')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_files_s3_key'), table_name='files', schema='file')
    op.drop_index(op.f('ix_file_files_id'), table_name='files', schema='file')
    op.drop_index(op.f('ix_file_files_file_name'), table_name='files', schema='file')
    op.drop_table('files', schema='file')
    op.drop_index(op.f('ix_shop_shops_id'), table_name='shops', schema='shop')
    op.drop_table('shops', schema='shop')
    op.drop_index(op.f('ix_account_ufos_id'), table_name='ufos', schema='account')
    op.drop_table('ufos', schema='account')
    op.drop_index(op.f('ix_account_users_id'), table_name='users', schema='account')
    op.drop_table('users', schema='account')
    # ### end Alembic commands ###
