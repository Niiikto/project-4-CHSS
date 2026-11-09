
-- ==================================================
-- WellnessIQ: Loneliness Analysis
-- Day 2: SQL 
-- Dataset: CHSS
-- ==================================================

-- 1. Count the total number of survey respondents

SELECT COUNT(*) AS total_respondents
FROM seniors;

-- 2. Count respondents from Ontario

SELECT COUNT(*) AS ontario_respondents
FROM seniors
WHERE province = 'Ontario';

-- 3. Display the first 10 respondents from British Columbia

SELECT ADM_RNO2, province, LONDVSCR
FROM seniors
WHERE province = 'British Columbia'
LIMIT 10;

-- 4. Find 5 respondents from British Columbia with the highest valid loneliness scores

SELECT ADM_RNO2, province, LONDVSCR
FROM seniors
WHERE province = 'British Columbia' AND LONDVSCR IS NOT NULL
ORDER BY LONDVSCR DESC
LIMIT 5;

-- 5. Calculate the average loneliness score for British Columbia

SELECT AVG(LONDVSCR) AS average_loneliness
FROM seniors
WHERE province = 'British Columbia';

-- 6. Count respondents in each province

SELECT province, COUNT(*) AS total_respondents
FROM seniors
GROUP BY province;

-- 7. Calculate average loneliness score for every province, highest to lowest

SELECT province, AVG(LONDVSCR) AS average_loneliness
FROM seniors
GROUP BY province
ORDER BY average_loneliness DESC;

-- 8. Final analysis: Average loneliness scores and valid responses for each province

SELECT province, ROUND(AVG(LONDVSCR), 2) AS average_loneliness, COUNT(LONDVSCR) AS valid_responses
FROM seniors
GROUP BY province
ORDER BY average_loneliness DESC;
