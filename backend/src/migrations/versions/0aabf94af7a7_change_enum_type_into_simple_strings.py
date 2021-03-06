"""change enum type into simple strings

Revision ID: 0aabf94af7a7
Revises: 135e6a9eaa01
Create Date: 2021-05-04 09:19:02.202952

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0aabf94af7a7'
down_revision = '135e6a9eaa01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags_messages')
    op.alter_column('evenements', 'type', type_=postgresql.VARCHAR(60))
    op.alter_column('messages', 'type', type_=postgresql.VARCHAR(60))
    op.alter_column('user_evenement_roles', 'type', type_=postgresql.VARCHAR(60))
    op.alter_column('messages_reactions', 'type', type_=postgresql.VARCHAR(60))
    op.alter_column('locations', 'type', type_=postgresql.VARCHAR(60))
    op.alter_column('groups', 'type', type_=postgresql.VARCHAR(60))
    op.alter_column('positions_groups', 'group_type', type_=postgresql.VARCHAR(60))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_locations_polygon', 'locations', ['polygon'], unique=False)
    op.create_index('idx_affairs_location', 'affairs', ['location'], unique=False)
    op.create_table('tags_messages',
    sa.Column('messages_uuid', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('tag_uuid', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['messages_uuid'], ['messages.uuid'], name='tags_messages_messages_uuid_fkey'),
    sa.ForeignKeyConstraint(['tag_uuid'], ['tags.uuid'], name='tags_messages_tag_uuid_fkey')
    )
    # ### end Alembic commands ###
