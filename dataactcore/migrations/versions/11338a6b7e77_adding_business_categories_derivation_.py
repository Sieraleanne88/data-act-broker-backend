"""Adding business categories derivation function

Revision ID: 11338a6b7e77
Revises: e26d14b0d235
Create Date: 2021-12-09 09:42:10.715687

"""

# revision identifiers, used by Alembic.
revision = '11338a6b7e77'
down_revision = 'e26d14b0d235'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
        create or replace function compile_fabs_business_categories(business_types text)
        returns text[]
        immutable parallel safe
        as $$
        declare
            bc_arr text[];
        begin

        -- BUSINESS (FOR-PROFIT ORGANIZATION)
            if business_types ~ '(R|23)'
            then
                bc_arr := bc_arr || array['small_business'];
            end if;

            if business_types ~ '(Q|22)'
            then
                bc_arr := bc_arr || array['other_than_small_business'];
            end if;

            if bc_arr && array['small_business', 'other_than_small_business']
            then
                bc_arr := bc_arr || array['category_business'];
            end if;

        -- NON-PROFIT
            if business_types ~ '(M|N|12)'
            then
                bc_arr := bc_arr || array['nonprofit'];
            end if;

        -- HIGHER EDUCATION
            if business_types ~ '(H|06)'
            then
                bc_arr := bc_arr || array['public_institution_of_higher_education'];
            end if;

            if business_types ~ '(O|20)'
            then
                bc_arr := bc_arr || array['private_institution_of_higher_education'];
            end if;

            if business_types ~ '(T|U|V|S)'
            then
                bc_arr := bc_arr || array['minority_serving_institution_of_higher_education'];
            end if;

            if bc_arr && array[
                'public_institution_of_higher_education',
                'private_institution_of_higher_education',
                'minority_serving_institution_of_higher_education'
            ]
            then
                bc_arr := bc_arr || array['higher_education'];
            end if;

        -- GOVERNMENT
            if business_types ~ '(A|00)'
            then
                bc_arr := bc_arr || array['regional_and_state_government'];
            end if;

            if business_types ~ '(E)'
            then
                bc_arr := bc_arr || array['regional_organization'];
            end if;

            if business_types ~ '(F)'
            then
                bc_arr := bc_arr || array['us_territory_or_possession'];
            end if;

            if business_types ~ '(B|C|D|G|01|02|04|05)'
            then
                bc_arr := bc_arr || array['local_government'];
            end if;

            if business_types ~ '(I|J|K|11)'
            then
                bc_arr := bc_arr || array['indian_native_american_tribal_government'];
            end if;

            if business_types ~ '(L)'
            then
                bc_arr := bc_arr || array['authorities_and_commissions'];
            end if;

            if bc_arr && array[
                'regional_and_state_government',
                'us_territory_or_possession',
                'local_government',
                'indian_native_american_tribal_government',
                'authorities_and_commissions',
                'regional_organization'
            ]
            then
                bc_arr := bc_arr || array['government'];
            end if;

        -- INDIVIDUALS
            if business_types ~ '(P|21)'
            then
                bc_arr := bc_arr || array['individuals'];
            end if;

            -- Sort and return the array.
            return array(select unnest(bc_arr) order by 1);
        end;
        $$  language plpgsql;
    """)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(""" DROP FUNCTION IF EXISTS compile_fabs_business_categories(TEXT) """)
    # ### end Alembic commands ###

