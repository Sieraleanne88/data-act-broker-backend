WITH aw_dap AS
    (SELECT DISTINCT ON (
            UPPER(dap.piid),
            UPPER(dap.parent_award_id),
            UPPER(dap.awarding_sub_tier_agency_c)
        )
        dap.unique_award_key AS unique_award_key,
        dap.piid AS piid,
        dap.idv_type AS idv_type,
        dap.parent_award_id AS parent_award_id,
        dap.award_description as award_description,
        dap.awarding_sub_tier_agency_c AS awarding_sub_tier_agency_c,
        dap.naics_description AS naics_description,
        dap.awarding_agency_code AS awarding_agency_code,
        dap.awarding_agency_name AS awarding_agency_name,
        dap.funding_agency_code AS funding_agency_code,
        dap.funding_agency_name AS funding_agency_name
    FROM detached_award_procurement AS dap
    WHERE EXISTS (
        SELECT 1
        FROM fsrs_procurement
        WHERE UPPER(TRANSLATE(fsrs_procurement.contract_number, '-', '')) = UPPER(TRANSLATE(dap.piid, '-', ''))
            AND UPPER(TRANSLATE(fsrs_procurement.idv_reference_number, '-', '')) IS NOT DISTINCT FROM UPPER(TRANSLATE(dap.parent_award_id, '-', ''))
            AND UPPER(fsrs_procurement.contracting_office_aid) = UPPER(dap.awarding_sub_tier_agency_c)
            AND fsrs_procurement.id {0} {1}
    )
    ORDER BY UPPER(dap.piid), UPPER(dap.parent_award_id), UPPER(dap.awarding_sub_tier_agency_c), dap.action_date)
INSERT INTO subaward (
    "unique_award_key",
    "award_id",
    "parent_award_id",
    "award_amount",
    "action_date",
    "fy",
    "awarding_agency_code",
    "awarding_agency_name",
    "awarding_sub_tier_agency_c",
    "awarding_sub_tier_agency_n",
    "awarding_office_code",
    "awarding_office_name",
    "funding_agency_code",
    "funding_agency_name",
    "funding_sub_tier_agency_co",
    "funding_sub_tier_agency_na",
    "funding_office_code",
    "funding_office_name",
    "awardee_or_recipient_uniqu",
    "awardee_or_recipient_legal",
    "dba_name",
    "ultimate_parent_unique_ide",
    "ultimate_parent_legal_enti",
    "legal_entity_country_code",
    "legal_entity_country_name",
    "legal_entity_address_line1",
    "legal_entity_city_name",
    "legal_entity_state_code",
    "legal_entity_state_name",
    "legal_entity_zip",
    "legal_entity_congressional",
    "legal_entity_foreign_posta",
    "business_types",
    "place_of_perform_city_name",
    "place_of_perform_state_code",
    "place_of_perform_state_name",
    "place_of_performance_zip",
    "place_of_perform_congressio",
    "place_of_perform_country_co",
    "place_of_perform_country_na",
    "award_description",
    "naics",
    "naics_description",
    "cfda_numbers",
    "cfda_titles",
    "subaward_type",
    "subaward_report_year",
    "subaward_report_month",
    "subaward_number",
    "subaward_amount",
    "sub_action_date",
    "sub_awardee_or_recipient_uniqu",
    "sub_awardee_or_recipient_legal",
    "sub_dba_name",
    "sub_ultimate_parent_unique_ide",
    "sub_ultimate_parent_legal_enti",
    "sub_legal_entity_country_code",
    "sub_legal_entity_country_name",
    "sub_legal_entity_address_line1",
    "sub_legal_entity_city_name",
    "sub_legal_entity_state_code",
    "sub_legal_entity_state_name",
    "sub_legal_entity_zip",
    "sub_legal_entity_congressional",
    "sub_legal_entity_foreign_posta",
    "sub_business_types",
    "sub_place_of_perform_city_name",
    "sub_place_of_perform_state_code",
    "sub_place_of_perform_state_name",
    "sub_place_of_performance_zip",
    "sub_place_of_perform_congressio",
    "sub_place_of_perform_country_co",
    "sub_place_of_perform_country_na",
    "subaward_description",
    "sub_high_comp_officer1_full_na",
    "sub_high_comp_officer1_amount",
    "sub_high_comp_officer2_full_na",
    "sub_high_comp_officer2_amount",
    "sub_high_comp_officer3_full_na",
    "sub_high_comp_officer3_amount",
    "sub_high_comp_officer4_full_na",
    "sub_high_comp_officer4_amount",
    "sub_high_comp_officer5_full_na",
    "sub_high_comp_officer5_amount",
    "prime_id",
    "internal_id",
    "date_submitted",
    "report_type",
    "transaction_type",
    "program_title",
    "contract_agency_code",
    "contract_idv_agency_code",
    "grant_funding_agency_id",
    "grant_funding_agency_name",
    "federal_agency_name",
    "treasury_symbol",
    "dunsplus4",
    "recovery_model_q1",
    "recovery_model_q2",
    "compensation_q1",
    "compensation_q2",
    "high_comp_officer1_full_na",
    "high_comp_officer1_amount",
    "high_comp_officer2_full_na",
    "high_comp_officer2_amount",
    "high_comp_officer3_full_na",
    "high_comp_officer3_amount",
    "high_comp_officer4_full_na",
    "high_comp_officer4_amount",
    "high_comp_officer5_full_na",
    "high_comp_officer5_amount",
    "place_of_perform_street",
    "sub_id",
    "sub_parent_id",
    "sub_federal_agency_id",
    "sub_federal_agency_name",
    "sub_funding_agency_id",
    "sub_funding_agency_name",
    "sub_funding_office_id",
    "sub_funding_office_name",
    "sub_naics",
    "sub_cfda_numbers",
    "sub_dunsplus4",
    "sub_recovery_subcontract_amt",
    "sub_recovery_model_q1",
    "sub_recovery_model_q2",
    "sub_compensation_q1",
    "sub_compensation_q2",
    "sub_place_of_perform_street",
    "created_at",
    "updated_at"
)
SELECT
    aw_dap.unique_award_key AS "unique_award_key",
    fsrs_procurement.contract_number AS "award_id",
    fsrs_procurement.idv_reference_number AS "parent_award_id",
    fsrs_procurement.dollar_obligated AS "award_amount",
    fsrs_procurement.date_signed AS "action_date",
    'FY' || fy(fsrs_procurement.date_signed) AS "fy",
    aw_dap.awarding_agency_code AS "awarding_agency_code",
    aw_dap.awarding_agency_name AS "awarding_agency_name",
    fsrs_procurement.contracting_office_aid AS "awarding_sub_tier_agency_c",
    fsrs_procurement.contracting_office_aname AS "awarding_sub_tier_agency_n",
    fsrs_procurement.contracting_office_id AS "awarding_office_code",
    fsrs_procurement.contracting_office_name AS "awarding_office_name",
    aw_dap.funding_agency_code AS "funding_agency_code",
    aw_dap.funding_agency_name AS "funding_agency_name",
    fsrs_procurement.funding_agency_id AS "funding_sub_tier_agency_co",
    fsrs_procurement.funding_agency_name AS "funding_sub_tier_agency_na",
    fsrs_procurement.funding_office_id AS "funding_office_code",
    fsrs_procurement.funding_office_name AS "funding_office_name",
    fsrs_procurement.duns AS "awardee_or_recipient_uniqu",
    fsrs_procurement.company_name AS "awardee_or_recipient_legal",
    fsrs_procurement.dba_name AS "dba_name",
    fsrs_procurement.parent_duns AS "ultimate_parent_unique_ide",
    fsrs_procurement.parent_company_name AS "ultimate_parent_legal_enti",
    le_country.country_code AS "legal_entity_country_code",
    le_country.country_name AS "legal_entity_country_name",
    fsrs_procurement.company_address_street AS "legal_entity_address_line1",
    fsrs_procurement.company_address_city AS "legal_entity_city_name",
    fsrs_procurement.company_address_state AS "legal_entity_state_code",
    fsrs_procurement.company_address_state_name AS "legal_entity_state_name",
    CASE WHEN fsrs_procurement.company_address_country = 'USA'
         THEN fsrs_procurement.company_address_zip
         ELSE NULL
    END AS "legal_entity_zip",
    fsrs_procurement.company_address_district AS "legal_entity_congressional",
    CASE WHEN fsrs_procurement.company_address_country <> 'USA'
         THEN fsrs_procurement.company_address_zip
         ELSE NULL
    END AS "legal_entity_foreign_posta",
    fsrs_procurement.bus_types AS "business_types",
    fsrs_procurement.principle_place_city AS "place_of_perform_city_name",
    fsrs_procurement.principle_place_state AS "place_of_perform_state_code",
    fsrs_procurement.principle_place_state_name AS "place_of_perform_state_name",
    fsrs_procurement.principle_place_zip AS "place_of_performance_zip",
    fsrs_procurement.principle_place_district AS "place_of_perform_congressio",
    ppop_country.country_code AS "place_of_perform_country_co",
    ppop_country.country_name AS "place_of_perform_country_na",
    aw_dap.award_description AS "award_description",
    fsrs_procurement.naics AS "naics",
    aw_dap.naics_description AS "naics_description",
    NULL AS "cfda_numbers",
    NULL AS "cfda_titles",

    -- File F Subawards
    'sub-contract' AS "subaward_type",
    fsrs_procurement.report_period_year AS "subaward_report_year",
    fsrs_procurement.report_period_mon AS "subaward_report_month",
    fsrs_subcontract.subcontract_num AS "subaward_number",
    fsrs_subcontract.subcontract_amount AS "subaward_amount",
    fsrs_subcontract.subcontract_date AS "sub_action_date",
    fsrs_subcontract.duns AS "sub_awardee_or_recipient_uniqu",
    fsrs_subcontract.company_name AS "sub_awardee_or_recipient_legal",
    fsrs_subcontract.dba_name AS "sub_dba_name",
    fsrs_subcontract.parent_duns AS "sub_ultimate_parent_unique_ide",
    fsrs_subcontract.parent_company_name AS "sub_ultimate_parent_legal_enti",
    sub_le_country.country_code AS "sub_legal_entity_country_code",
    sub_le_country.country_name AS "sub_legal_entity_country_name",
    fsrs_subcontract.company_address_street AS "sub_legal_entity_address_line1",
    fsrs_subcontract.company_address_city AS "sub_legal_entity_city_name",
    fsrs_subcontract.company_address_state AS "sub_legal_entity_state_code",
    fsrs_subcontract.company_address_state_name AS "sub_legal_entity_state_name",
    CASE WHEN fsrs_subcontract.company_address_country = 'USA'
         THEN fsrs_subcontract.company_address_zip
         ELSE NULL
    END AS "sub_legal_entity_zip",
    fsrs_subcontract.company_address_district AS "sub_legal_entity_congressional",
    CASE WHEN fsrs_subcontract.company_address_country <> 'USA'
         THEN fsrs_subcontract.company_address_zip
         ELSE NULL
    END AS "sub_legal_entity_foreign_posta",
    fsrs_subcontract.bus_types AS "sub_business_types",
    fsrs_subcontract.principle_place_city AS "sub_place_of_perform_city_name",
    fsrs_subcontract.principle_place_state AS "sub_place_of_perform_state_code",
    fsrs_subcontract.principle_place_state_name AS "sub_place_of_perform_state_name",
    fsrs_subcontract.principle_place_zip AS "sub_place_of_performance_zip",
    fsrs_subcontract.principle_place_district AS "sub_place_of_perform_congressio",
    sub_ppop_country.country_code AS "sub_place_of_perform_country_co",
    sub_ppop_country.country_name AS "sub_place_of_perform_country_na",
    fsrs_subcontract.overall_description AS "subaward_description",
    fsrs_subcontract.top_paid_fullname_1 AS "sub_high_comp_officer1_full_na",
    fsrs_subcontract.top_paid_amount_1 AS "sub_high_comp_officer1_amount",
    fsrs_subcontract.top_paid_fullname_2 AS "sub_high_comp_officer2_full_na",
    fsrs_subcontract.top_paid_amount_2 AS "sub_high_comp_officer2_amount",
    fsrs_subcontract.top_paid_fullname_3 AS "sub_high_comp_officer3_full_na",
    fsrs_subcontract.top_paid_amount_3 AS "sub_high_comp_officer3_amount",
    fsrs_subcontract.top_paid_fullname_4 AS "sub_high_comp_officer4_full_na",
    fsrs_subcontract.top_paid_amount_4 AS "sub_high_comp_officer4_amount",
    fsrs_subcontract.top_paid_fullname_5 AS "sub_high_comp_officer5_full_na",
    fsrs_subcontract.top_paid_amount_5 AS "sub_high_comp_officer5_amount",

    -- File F Prime Awards
    fsrs_procurement.id AS "prime_id",
    fsrs_procurement.internal_id AS "internal_id",
    fsrs_procurement.date_submitted AS "date_submitted",
    fsrs_procurement.report_type AS "report_type",
    fsrs_procurement.transaction_type AS "transaction_type",
    fsrs_procurement.program_title AS "program_title",
    fsrs_procurement.contract_agency_code AS "contract_agency_code",
    fsrs_procurement.contract_idv_agency_code AS "contract_idv_agency_code",
    NULL AS "grant_funding_agency_id",
    NULL AS "grant_funding_agency_name",
    NULL AS "federal_agency_name",
    fsrs_procurement.treasury_symbol AS "treasury_symbol",
    NULL AS "dunsplus4",
    fsrs_procurement.recovery_model_q1 AS "recovery_model_q1",
    fsrs_procurement.recovery_model_q2 AS "recovery_model_q2",
    NULL AS "compensation_q1",
    NULL AS "compensation_q2",
    fsrs_procurement.top_paid_fullname_1 AS "high_comp_officer1_full_na",
    fsrs_procurement.top_paid_amount_1 AS "high_comp_officer1_amount",
    fsrs_procurement.top_paid_fullname_2 AS "high_comp_officer2_full_na",
    fsrs_procurement.top_paid_amount_2 AS "high_comp_officer2_amount",
    fsrs_procurement.top_paid_fullname_3 AS "high_comp_officer3_full_na",
    fsrs_procurement.top_paid_amount_3 AS "high_comp_officer3_amount",
    fsrs_procurement.top_paid_fullname_4 AS "high_comp_officer4_full_na",
    fsrs_procurement.top_paid_amount_4 AS "high_comp_officer4_amount",
    fsrs_procurement.top_paid_fullname_5 AS "high_comp_officer5_full_na",
    fsrs_procurement.top_paid_amount_5 AS "high_comp_officer5_amount",
    fsrs_procurement.principle_place_street AS "place_of_perform_street",

    -- File F Subawards
    fsrs_subcontract.id AS "sub_id",
    fsrs_subcontract.parent_id AS "sub_parent_id",
    NULL AS "sub_federal_agency_id",
    NULL AS "sub_federal_agency_name",
    fsrs_subcontract.funding_agency_id AS "sub_funding_agency_id",
    fsrs_subcontract.funding_agency_name AS "sub_funding_agency_name",
    fsrs_subcontract.funding_office_id AS "sub_funding_office_id",
    fsrs_subcontract.funding_office_name AS "sub_funding_office_name",
    fsrs_subcontract.naics AS "sub_naics",
    NULL AS "sub_cfda_numbers",
    NULL AS "sub_dunsplus4",
    fsrs_subcontract.recovery_subcontract_amt AS "sub_recovery_subcontract_amt",
    fsrs_subcontract.recovery_model_q1 AS "sub_recovery_model_q1",
    fsrs_subcontract.recovery_model_q2 AS "sub_recovery_model_q2",
    NULL AS "sub_compensation_q1",
    NULL AS "sub_compensation_q2",
    fsrs_subcontract.principle_place_street AS "sub_place_of_perform_street",

    NOW() AS "created_at",
    NOW() AS "updated_at"

FROM fsrs_procurement
    JOIN fsrs_subcontract
        ON fsrs_subcontract.parent_id = fsrs_procurement.id
    LEFT OUTER JOIN aw_dap
        ON UPPER(TRANSLATE(fsrs_procurement.contract_number, '-', '')) = UPPER(TRANSLATE(aw_dap.piid, '-', ''))
        AND UPPER(TRANSLATE(fsrs_procurement.idv_reference_number, '-', '')) IS NOT DISTINCT FROM UPPER(TRANSLATE(aw_dap.parent_award_id, '-', ''))
        AND UPPER(fsrs_procurement.contracting_office_aid) = UPPER(aw_dap.awarding_sub_tier_agency_c)
    LEFT OUTER JOIN country_code AS le_country
        ON (UPPER(fsrs_procurement.company_address_country) = UPPER(le_country.country_code)
            OR UPPER(fsrs_procurement.company_address_country) = UPPER(le_country.country_code_2_char))
    LEFT OUTER JOIN country_code AS ppop_country
        ON (UPPER(fsrs_procurement.principle_place_country) = UPPER(ppop_country.country_code)
            OR UPPER(fsrs_procurement.principle_place_country) = UPPER(ppop_country.country_code_2_char))
    LEFT OUTER JOIN country_code AS sub_le_country
        ON (UPPER(fsrs_subcontract.company_address_country) = UPPER(sub_le_country.country_code)
            OR UPPER(fsrs_subcontract.company_address_country) = UPPER(sub_le_country.country_code_2_char))
    LEFT OUTER JOIN country_code AS sub_ppop_country
        ON (UPPER(fsrs_subcontract.principle_place_country) = UPPER(sub_ppop_country.country_code)
            OR UPPER(fsrs_subcontract.principle_place_country) = UPPER(sub_ppop_country.country_code_2_char))
WHERE fsrs_procurement.id {0} {1}
