"""init

Revision ID: dc0a317f2adb
Revises: 
Create Date: 2021-06-13 20:09:56.259428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc0a317f2adb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'PERSONAL_DATA',
        sa.Column('id', sa.Integer, primary_key=True, index = True),
        sa.Column('cpf', sa.BigInteger, unique=True, nullable = False),
        sa.Column('name', sa.String, nullable = False),
        sa.Column('surname', sa.String, nullable = False),
        sa.Column('age', sa.Integer),
        sa.Column('creditcard_id', sa.BigInteger),
        sa.Column('phone', sa.BigInteger)
    )
    op.create_table(
        'ADDRESS_DATA',
        sa.Column('id', sa.Integer, primary_key=True, index = True),
        sa.Column('postal_code', sa.BigInteger, nullable = False),
        sa.Column('number', sa.Integer, nullable = False),
        sa.Column('street', sa.String, nullable = False),
        sa.Column('district', sa.String, nullable = False),
        sa.Column('city_id', sa.String, nullable = False),
        sa.Column('country', sa.String, nullable = False),
        sa.Column('last_update', sa.Date, nullable = False),
        sa.Column('cpf', sa.BigInteger, unique=True, nullable = False),
    )
    op.create_table(
        'DEBT_DATA',
        sa.Column('id', sa.Integer, primary_key=True, index = True),
        sa.Column('creditor', sa.String),
        sa.Column('debt_amount', sa.Float),
        sa.Column('interest_rate', sa.Float),
        sa.Column('cpf', sa.BigInteger, nullable = False),
    )
    op.create_table(
        'APP_USERS',
        sa.Column('id', sa.Integer, primary_key=True, index = True),
        sa.Column('login', sa.String),
        sa.Column('email', sa.String),
        sa.Column('cpf', sa.BigInteger),
        sa.Column('password', sa.String),
    )


def downgrade():
    op.drop_table('PERSONAL_DATA')
    op.drop_table('ADDRESS_DATA')
    op.drop_table('DEBT_DATA')
    op.drop_table('APP_USERS')
