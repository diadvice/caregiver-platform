/*
 * Part 2: SQL Queries Implementation
 * All queries required for the project in pure SQL
 */

-- =============================================================================
-- 3. UPDATE SQL STATEMENTS
-- =============================================================================

-- 3.1 Update the phone number of Arman Armanov to +77773414141
UPDATE users
SET phone_number = '+77773414141'
WHERE given_name = 'Arman' AND surname = 'Armanov';

-- 3.2 Add $0.3 commission fee to hourly rate if < $10, or 10% if >= $10
UPDATE caregivers
SET hourly_rate = CASE
    WHEN hourly_rate < 10 THEN hourly_rate + 0.3
    ELSE hourly_rate * 1.10
END;

-- =============================================================================
-- 4. DELETE SQL STATEMENTS
-- =============================================================================

-- 4.1 Delete the jobs posted by Amina Aminova
DELETE FROM jobs
WHERE member_user_id = (
    SELECT user_id
    FROM users
    WHERE given_name = 'Amina' AND surname = 'Aminova'
);

-- 4.2 Delete all members who live on Kabanbay Batyr street
DELETE FROM users
WHERE user_id IN (
    SELECT member_user_id
    FROM addresses
    WHERE street = 'Kabanbay Batyr'
);
-- =============================================================================
-- 5. SIMPLE QUERIES
-- =============================================================================

-- 5.1 Select caregiver and member names for the accepted appointments
SELECT 
    u_caregiver.given_name AS caregiver_name,
    u_caregiver.surname AS caregiver_surname,
    u_member.given_name AS member_name,
    u_member.surname AS member_surname,
    a.appointment_date
FROM appointments a
JOIN caregivers c ON c.caregiver_user_id = a.caregiver_user_id
JOIN users u_caregiver ON u_caregiver.user_id = c.caregiver_user_id
JOIN members m ON m.member_user_id = a.member_user_id
JOIN users u_member ON u_member.user_id = m.member_user_id
WHERE a.status = 'accepted';

-- 5.2 List job ids that contain 'soft-spoken' in their other requirements
SELECT job_id, required_caregiving_type, other_requirements
FROM jobs
WHERE other_requirements LIKE '%soft-spoken%';

-- 5.3 List the work hours of all babysitter positions
SELECT 
    a.appointment_id,
    a.work_hours,
    a.appointment_date
FROM appointments a
JOIN caregivers c ON c.caregiver_user_id = a.caregiver_user_id
WHERE c.caregiving_type = 'Babysitter';

-- 5.4 List members looking for Elderly Care in Astana with 'No pets.' rule
SELECT DISTINCT
    u.user_id,
    u.given_name,
    u.surname,
    u.city,
    m.house_rules
FROM users u
JOIN members m ON m.member_user_id = u.user_id
JOIN jobs j ON j.member_user_id = m.member_user_id
WHERE u.city = 'Astana'
    AND m.house_rules LIKE '%No pets.%'
    AND j.required_caregiving_type = 'Elderly Care';

-- =============================================================================
-- 6. COMPLEX QUERIES
-- =============================================================================

-- 6.1 Count the number of applicants for each job posted by a member
SELECT 
    j.job_id,
    j.required_caregiving_type,
    u.given_name AS member_name,
    u.surname AS member_surname,
    COUNT(ja.caregiver_user_id) AS applicant_count
FROM jobs j
JOIN members m ON m.member_user_id = j.member_user_id
JOIN users u ON u.user_id = m.member_user_id
LEFT JOIN job_applications ja ON ja.job_id = j.job_id
GROUP BY j.job_id, j.required_caregiving_type, u.given_name, u.surname
ORDER BY j.job_id;

-- 6.2 Total hours spent by caregivers for all accepted appointments
SELECT 
    u.given_name AS caregiver_name,
    u.surname AS caregiver_surname,
    c.caregiving_type,
    SUM(a.work_hours) AS total_hours
FROM caregivers c
JOIN users u ON u.user_id = c.caregiver_user_id
JOIN appointments a ON a.caregiver_user_id = c.caregiver_user_id
WHERE a.status = 'accepted'
GROUP BY u.given_name, u.surname, c.caregiving_type
ORDER BY total_hours DESC;

-- 6.3 Average pay of caregivers based on accepted appointments
SELECT 
    u.given_name AS caregiver_name,
    u.surname AS caregiver_surname,
    c.hourly_rate,
    AVG(a.work_hours) AS avg_hours,
    c.hourly_rate * AVG(a.work_hours) AS avg_pay
FROM caregivers c
JOIN users u ON u.user_id = c.caregiver_user_id
JOIN appointments a ON a.caregiver_user_id = c.caregiver_user_id
WHERE a.status = 'accepted'
GROUP BY u.given_name, u.surname, c.hourly_rate
ORDER BY avg_pay DESC;

-- 6.4 Caregivers who earn above average based on accepted appointments
WITH avg_earnings AS (
    SELECT AVG(c.hourly_rate * a.work_hours) AS overall_avg
    FROM caregivers c
    JOIN appointments a ON a.caregiver_user_id = c.caregiver_user_id
    WHERE a.status = 'accepted'
)
SELECT 
    u.given_name AS caregiver_name,
    u.surname AS caregiver_surname,
    c.hourly_rate,
    SUM(c.hourly_rate * a.work_hours) AS total_earnings,
    COUNT(a.appointment_id) AS appointment_count,
    AVG(c.hourly_rate * a.work_hours) AS avg_per_appointment
FROM caregivers c
JOIN users u ON u.user_id = c.caregiver_user_id
JOIN appointments a ON a.caregiver_user_id = c.caregiver_user_id
WHERE a.status = 'accepted'
GROUP BY u.given_name, u.surname, c.hourly_rate, c.caregiver_user_id
HAVING AVG(c.hourly_rate * a.work_hours) > (SELECT overall_avg FROM avg_earnings)
ORDER BY total_earnings DESC;

-- =============================================================================
-- 7. QUERY WITH DERIVED ATTRIBUTE
-- =============================================================================

-- 7. Calculate the total cost to pay for a caregiver for all accepted appointments
SELECT 
    u.given_name AS caregiver_name,
    u.surname AS caregiver_surname,
    c.caregiving_type,
    c.hourly_rate,
    SUM(a.work_hours) AS total_hours,
    SUM(c.hourly_rate * a.work_hours) AS total_cost
FROM caregivers c
JOIN users u ON u.user_id = c.caregiver_user_id
JOIN appointments a ON a.caregiver_user_id = c.caregiver_user_id
WHERE a.status = 'accepted'
GROUP BY u.given_name, u.surname, c.caregiving_type, c.hourly_rate
ORDER BY total_cost DESC;

-- =============================================================================
-- 8. VIEW OPERATION
-- =============================================================================

-- 8. Create view for all job applications and the applicants
CREATE OR REPLACE VIEW job_applications_view AS
SELECT 
    ja.caregiver_user_id,
    ja.job_id,
    ja.date_applied,
    u_caregiver.given_name AS applicant_name,
    u_caregiver.surname AS applicant_surname,
    j.required_caregiving_type,
    j.other_requirements,
    u_member.given_name AS member_name,
    u_member.surname AS member_surname,
    j.date_posted
FROM job_applications ja
JOIN caregivers c ON c.caregiver_user_id = ja.caregiver_user_id
JOIN users u_caregiver ON u_caregiver.user_id = c.caregiver_user_id
JOIN jobs j ON j.job_id = ja.job_id
JOIN members m ON m.member_user_id = j.member_user_id
JOIN users u_member ON u_member.user_id = m.member_user_id;

-- Query to view all job applications
SELECT * FROM job_applications_view
ORDER BY date_applied DESC;
