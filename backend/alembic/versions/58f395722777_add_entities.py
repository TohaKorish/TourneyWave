"""add entities

Revision ID: 58f395722777
Revises: 9ddb72de2d6a
Create Date: 2024-10-22 09:32:09.408354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58f395722777'
down_revision: Union[str, None] = '9ddb72de2d6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('participant_count', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matches',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'ACTIVATED', 'OPEN', 'COMPLETED', name='matchstatusenum'), nullable=False),
    sa.Column('connection_key', sa.String(length=255), nullable=False),
    sa.Column('connection_description', sa.Text(), nullable=False),
    sa.Column('stream_url', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=30), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_team',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_team')
    op.drop_table('matches')
    op.drop_table('teams')
    op.drop_table('games')
    # ### end Alembic commands ###
