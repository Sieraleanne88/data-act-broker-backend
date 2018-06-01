"""Update program activity to store fiscal_year_quarter and remove budget_year

Revision ID: de48ea53b63c
Revises: 321af67fae11
Create Date: 2018-05-31 11:43:16.693958

"""

# revision identifiers, used by Alembic.
revision = 'de48ea53b63c'
down_revision = '321af67fae11'
branch_labels = None
depends_on = None

import os

from alembic import op
import sqlalchemy as sa

from dataactcore.config import CONFIG_BROKER
from dataactcore.models.domainModels import ProgramActivity
from dataactcore.interfaces.db import GlobalDB
from dataactvalidator.scripts.load_program_activity import load_program_activity_data


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_pa_tas_pa', table_name='program_activity')
    op.drop_index('ix_program_activity_budget_year', table_name='program_activity')

    op.alter_column('program_activity', 'budget_year', new_column_name='fiscal_year_quarter')
    op.create_index(op.f('ix_program_activity_fiscal_year_quarter'), 'program_activity', ['fiscal_year_quarter'], unique=False)

    op.create_index('ix_pa_tas_pa', 'program_activity', ['fiscal_year_quarter', 'agency_id', 'allocation_transfer_id', 'account_number', 'program_activity_code', 'program_activity_name'], unique=True)

    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_pa_tas_pa', table_name='program_activity')
    op.drop_index(op.f('ix_program_activity_fiscal_year_quarter'), table_name='program_activity')

    op.alter_column('program_activity', 'fiscal_year_quarter', new_column_name='budget_year')
    op.create_index('ix_program_activity_budget_year', 'program_activity', ['budget_year'], unique=False)

    op.create_index('ix_pa_tas_pa', 'program_activity', ['budget_year', 'agency_id', 'allocation_transfer_id', 'account_number', 'program_activity_code', 'program_activity_name'], unique=True)

    # ### end Alembic commands ###

