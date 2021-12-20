-- The combination of TAS/object class/program activity code+name/reimbursable flag/DEFC in File B (object class program
-- activity) should be unique
SELECT
    row_number,
    beginning_period_of_availa,
    ending_period_of_availabil,
    agency_identifier,
    allocation_transfer_agency,
    availability_type_code,
    main_account_code,
    sub_account_code,
    object_class,
    program_activity_code,
    by_direct_reimbursable_fun,
    disaster_emergency_fund_code,
    display_tas AS "uniqueid_TAS",
    program_activity_code AS "uniqueid_ProgramActivityCode",
    program_activity_name AS "uniqueid_ProgramActivityName",
    object_class AS "uniqueid_ObjectClass",
    by_direct_reimbursable_fun AS "uniqueid_ByDirectReimbursableFundingSource",
    disaster_emergency_fund_code AS "uniqueid_DisasterEmergencyFundCode"
FROM (
    SELECT op.row_number,
        op.beginning_period_of_availa,
        op.ending_period_of_availabil,
        op.agency_identifier,
        op.allocation_transfer_agency,
        UPPER(op.availability_type_code) AS availability_type_code,
        op.main_account_code,
        op.sub_account_code,
        op.object_class,
        op.program_activity_code,
        UPPER(op.program_activity_name) AS program_activity_name,
        UPPER(op.by_direct_reimbursable_fun) AS by_direct_reimbursable_fun,
        op.submission_id,
        op.tas,
        op.display_tas,
        UPPER(op.disaster_emergency_fund_code) AS disaster_emergency_fund_code,
        -- numbers all instances of this unique combination incrementally (1, 2, 3, etc)
        ROW_NUMBER() OVER (PARTITION BY
            op.beginning_period_of_availa,
            op.ending_period_of_availabil,
            op.agency_identifier,
            op.allocation_transfer_agency,
            UPPER(op.availability_type_code),
            op.main_account_code,
            op.sub_account_code,
            op.object_class,
            op.program_activity_code,
            UPPER(op.program_activity_name),
            UPPER(op.by_direct_reimbursable_fun),
            UPPER(op.disaster_emergency_fund_code)
            ORDER BY op.row_number
        ) AS row
    FROM object_class_program_activity AS op
    WHERE op.submission_id = {0}
    ) duplicates
-- if there is any row numbered over 1, that means there's more than one instance of that unique combination
WHERE duplicates.row > 1;
