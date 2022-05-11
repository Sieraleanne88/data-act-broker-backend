-- When provided, AwardeeOrRecipientUEI must be registered (not necessarily active) in SAM, unless the ActionDate is
-- before October 1, 2010.
WITH fabs31_4_1_{0} AS
    (SELECT unique_award_key,
        row_number,
        assistance_type,
        action_date,
        uei,
        afa_generated_unique
    FROM fabs
    WHERE submission_id = {0}
        AND (CASE WHEN is_date(COALESCE(action_date, '0'))
             THEN CAST(action_date AS DATE)
             END) > CAST('10/01/2010' AS DATE)
        AND COALESCE(fabs.uei, '') <> ''
        AND NOT EXISTS (
            SELECT 1
            FROM sam_recipient
            WHERE UPPER(fabs.uei) = UPPER(sam_recipient.uei)
        )
        AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D'),
min_dates_{0} AS
    (SELECT unique_award_key,
        MIN(cast_as_date(action_date)) AS min_date
    FROM published_fabs AS pf
    WHERE is_active IS TRUE
        AND EXISTS (
            SELECT 1
            FROM fabs31_4_1_{0} AS fabs
            WHERE pf.unique_award_key = fabs.unique_award_key
        )
    GROUP BY unique_award_key)
SELECT
    row_number,
    assistance_type,
    action_date,
    uei,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM fabs31_4_1_{0} AS fabs
LEFT JOIN min_dates_{0} AS md
    ON fabs.unique_award_key = md.unique_award_key;
