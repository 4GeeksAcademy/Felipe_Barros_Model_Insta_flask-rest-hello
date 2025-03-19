"""empty message

Revision ID: de2de33cddfe
Revises: a5cffa318ac2
Create Date: 2025-03-19 11:47:39.697576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de2de33cddfe'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follower',
    sa.Column('user_from_id', sa.Integer(), nullable=False),
    sa.Column('user_to_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_from_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_to_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_from_id', 'user_to_id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment_text', sa.String(length=100), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', sa.Enum('image', 'video', 'audio', name='media_types'), nullable=False),
    sa.Column('url', sa.String(length=1000), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('firstname', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('lastname', sa.String(length=50), nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=100),
               nullable=True)
        batch_op.drop_column('is_active')
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.drop_column('lastname')
        batch_op.drop_column('firstname')
        batch_op.drop_column('username')

    op.drop_table('media')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('follower')
    # ### end Alembic commands ###
