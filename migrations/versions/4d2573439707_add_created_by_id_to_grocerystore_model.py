"""Add created_by_id to GroceryStore model

Revision ID: 4d2573439707
Revises: 
Create Date: 2024-02-14 10:53:00.720272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d2573439707'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('grocery_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by_id', sa.Integer()))
        batch_op.create_foreign_key('fk_grocery_item_created_by_id', 'user', ['created_by_id'], ['id'])

    with op.batch_alter_table('grocery_store', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by_id', sa.Integer()))
        batch_op.create_foreign_key('fk_grocery_store_created_by_id', 'user', ['created_by_id'], ['id'])



    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)

    with op.batch_alter_table('grocery_store', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('created_by_id')

    with op.batch_alter_table('grocery_item', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('created_by_id')

    op.create_table('_alembic_tmp_grocery_item',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), nullable=False),
    sa.Column('price', sa.FLOAT(), nullable=False),
    sa.Column('category', sa.VARCHAR(length=7), nullable=True),
    sa.Column('photo_url', sa.TEXT(), nullable=True),
    sa.Column('store_id', sa.INTEGER(), nullable=False),
    sa.Column('created_by_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], name='fk_grocery_item_created_by_id'),
    sa.ForeignKeyConstraint(['store_id'], ['grocery_store.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
