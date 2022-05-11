-- For PrimaryPlaceOfPerformanceCode XX##### or XX####R, where PrimaryPlaceOfPerformanceZIP+4 is "city-wide":
-- city code ##### or ####R must be valid and exist in the provided state.
WITH detached_award_financial_assistance_fabs41_1_{0} AS
    (SELECT submission_id,
        row_number,
        place_of_performance_code,
        place_of_performance_zip4a,
        correction_delete_indicatr,
        afa_generated_unique
    FROM detached_award_financial_assistance
    WHERE submission_id = {0})
SELECT
    dafa.row_number,
    dafa.place_of_performance_code,
    dafa.afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance_fabs41_1_{0} AS dafa
WHERE UPPER(dafa.place_of_performance_code) ~ '^[A-Z][A-Z]\d\d\d\d[\dR]$'
    AND (COALESCE(dafa.place_of_performance_zip4a, '') = ''
         OR dafa.place_of_performance_zip4a = 'city-wide'
    )
    AND dafa.row_number NOT IN (
        SELECT DISTINCT sub_dafa.row_number
        FROM detached_award_financial_assistance_fabs41_1_{0} AS sub_dafa
        JOIN city_code
            ON SUBSTRING(sub_dafa.place_of_performance_code, 3, 5) = city_code.city_code
                AND UPPER(SUBSTRING(sub_dafa.place_of_performance_code, 1, 2)) = city_code.state_code
    )
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
