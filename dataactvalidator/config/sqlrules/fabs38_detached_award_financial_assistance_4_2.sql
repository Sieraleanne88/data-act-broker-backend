-- For new modifications to existing awards, we derive AwardingOfficeCode from the original transaction establishing the
-- award, when it is provided there and not provided in the new modification. For this row, we are declining to derive
-- the AwardingOfficeCode from the original transaction establishing the award because the AwardingOfficeCode is either
-- not present in the Federal Hierarchy or not specifically designated as an Assistance Awarding Office there. If the
-- code you are providing in this row is accurate, please update the Federal Hierarchy to include it and flag it as an
-- Assistance Awarding Office. If it is not accurate, please correct the original award transaction to reference a
-- valid Financial Assistance Awarding AAC/office code in the hierarchy.
WITH detached_award_financial_assistance_38_4_2_{0} AS
    (SELECT unique_award_key,
    	row_number,
    	awarding_office_code,
    	award_modification_amendme,
    	afa_generated_unique
    FROM detached_award_financial_assistance AS dafa
    WHERE dafa.submission_id = {0}
        AND UPPER(COALESCE(dafa.correction_delete_indicatr, '')) <> 'D'
        AND COALESCE(awarding_office_code, '') = ''),
min_dates_{0} AS
    (SELECT unique_award_key,
        MIN(cast_as_date(action_date)) AS min_date
    FROM published_award_financial_assistance AS pafa
    WHERE is_active IS TRUE
        AND EXISTS (
            SELECT 1
            FROM detached_award_financial_assistance_38_4_2_{0} AS dafa
            WHERE pafa.unique_award_key = dafa.unique_award_key)
    GROUP BY unique_award_key),
awarding_codes_{0} AS
	(SELECT pafa.unique_award_key,
		pafa.awarding_office_code,
		pafa.award_modification_amendme
	FROM published_award_financial_assistance AS pafa
	JOIN min_dates_{0} AS md
		ON md.unique_award_key = pafa.unique_award_key
			AND md.min_date = cast_as_date(pafa.action_date)
	WHERE COALESCE(pafa.awarding_office_code, '') <> ''
	    AND pafa.is_active IS TRUE)
SELECT
    row_number,
    awarding_office_code,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance_38_4_2_{0} AS dafa
WHERE EXISTS (
	SELECT 1
	FROM awarding_codes_{0} AS ac
	WHERE dafa.unique_award_key = ac.unique_award_key
		AND COALESCE(dafa.award_modification_amendme, '') <> COALESCE(ac.award_modification_amendme, '')
		AND NOT EXISTS (
			SELECT 1
			FROM office
			WHERE UPPER(ac.awarding_office_code) = UPPER(office.office_code)
			    AND office.financial_assistance_awards_office IS TRUE));
