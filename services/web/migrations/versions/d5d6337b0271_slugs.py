"""slugs

Revision ID: d5d6337b0271
Revises: bec0dda6be5e
Create Date: 2021-06-22 15:22:16.198539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5d6337b0271'
down_revision = 'bec0dda6be5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('title', sa.String(), nullable=False))
    op.add_column('course', sa.Column('slug', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'course', ['title'])
    op.create_unique_constraint(None, 'course', ['slug'])
    op.drop_column('course', 'name')
    op.add_column('lesson', sa.Column('title', sa.String(), nullable=False))
    op.add_column('lesson', sa.Column('slug', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'lesson', ['title'])
    op.create_unique_constraint(None, 'lesson', ['slug'])
    op.drop_column('lesson', 'name')
    op.add_column('program', sa.Column('title', sa.String(), nullable=False))
    op.add_column('program', sa.Column('slug', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'program', ['slug'])
    op.create_unique_constraint(None, 'program', ['title'])
    op.drop_column('program', 'name')
    op.add_column('section', sa.Column('title', sa.String(), nullable=False))
    op.add_column('section', sa.Column('slug', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'section', ['slug'])
    op.create_unique_constraint(None, 'section', ['title'])
    op.create_unique_constraint(None, 'user', ['email'])
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'section', type_='unique')
    op.drop_constraint(None, 'section', type_='unique')
    op.drop_column('section', 'slug')
    op.drop_column('section', 'title')
    op.add_column('program', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'program', type_='unique')
    op.drop_constraint(None, 'program', type_='unique')
    op.drop_column('program', 'slug')
    op.drop_column('program', 'title')
    op.add_column('lesson', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'lesson', type_='unique')
    op.drop_constraint(None, 'lesson', type_='unique')
    op.drop_column('lesson', 'slug')
    op.drop_column('lesson', 'title')
    op.add_column('course', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'course', type_='unique')
    op.drop_constraint(None, 'course', type_='unique')
    op.drop_column('course', 'slug')
    op.drop_column('course', 'title')
    # ### end Alembic commands ###
