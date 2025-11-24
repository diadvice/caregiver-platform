--
-- PostgreSQL database dump
-- Caregiving Management System
--

-- Drop tables if they exist
DROP TABLE IF EXISTS appointments CASCADE;
DROP TABLE IF EXISTS job_applications CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS addresses CASCADE;
DROP TABLE IF EXISTS members CASCADE;
DROP TABLE IF EXISTS caregivers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create tables
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE caregivers (
    caregiver_user_id INTEGER PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    photo VARCHAR(255),
    gender VARCHAR(20),
    caregiving_type VARCHAR(50) NOT NULL,
    hourly_rate NUMERIC(10, 2) NOT NULL
);

CREATE TABLE members (
    member_user_id INTEGER PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    house_rules TEXT,
    dependent_description TEXT
);

CREATE TABLE addresses (
    member_user_id INTEGER NOT NULL REFERENCES members(member_user_id) ON DELETE CASCADE,
    house_number VARCHAR(20) NOT NULL,
    street VARCHAR(100) NOT NULL,
    town VARCHAR(100) NOT NULL,
    PRIMARY KEY (member_user_id, house_number, street, town)
);

CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    member_user_id INTEGER NOT NULL REFERENCES members(member_user_id) ON DELETE CASCADE,
    required_caregiving_type VARCHAR(50) NOT NULL,
    other_requirements TEXT,
    date_posted DATE NOT NULL
);

CREATE TABLE job_applications (
    caregiver_user_id INTEGER NOT NULL REFERENCES caregivers(caregiver_user_id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    date_applied DATE NOT NULL,
    PRIMARY KEY (caregiver_user_id, job_id)
);

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INTEGER NOT NULL REFERENCES caregivers(caregiver_user_id) ON DELETE CASCADE,
    member_user_id INTEGER NOT NULL REFERENCES members(member_user_id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours NUMERIC(5, 2) NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- Insert sample data

-- Insert Users (20 users)
INSERT INTO users (email, given_name, surname, city, phone_number, profile_description, password) VALUES
('sarah.johnson@email.com', 'Sarah', 'Johnson', 'Astana', '+77011234567', 'Experienced babysitter with 5 years of experience.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('mike.peterson@email.com', 'Mike', 'Peterson', 'Almaty', '+77011234568', 'Certified elderly care specialist.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('emma.wilson@email.com', 'Emma', 'Wilson', 'Astana', '+77011234569', 'Professional playmate for children.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('david.brown@email.com', 'David', 'Brown', 'Shymkent', '+77011234570', 'Loving babysitter with pediatric first aid training.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('lisa.anderson@email.com', 'Lisa', 'Anderson', 'Astana', '+77011234571', 'Patient elderly caregiver with nursing background.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('john.martinez@email.com', 'John', 'Martinez', 'Almaty', '+77011234572', 'Fun and energetic playmate for kids.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('anna.taylor@email.com', 'Anna', 'Taylor', 'Astana', '+77011234573', 'Reliable babysitter with references.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('robert.thomas@email.com', 'Robert', 'Thomas', 'Karaganda', '+77011234574', 'Compassionate elderly care provider.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('maria.garcia@email.com', 'Maria', 'Garcia', 'Astana', '+77011234575', 'Creative playmate with art education.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('james.lee@email.com', 'James', 'Lee', 'Almaty', '+77011234576', 'Experienced babysitter for infants and toddlers.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('amina.aminova@email.com', 'Amina', 'Aminova', 'Astana', '+77011234577', 'Looking for reliable childcare.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('arman.armanov@email.com', 'Arman', 'Armanov', 'Almaty', '+77011234578', 'Need elderly care for my mother.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('diana.kim@email.com', 'Diana', 'Kim', 'Astana', '+77011234579', 'Seeking playmate for my 6-year-old.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('nurlan.bekov@email.com', 'Nurlan', 'Bekov', 'Shymkent', '+77011234580', 'Need babysitter for weekends.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('zarina.saparova@email.com', 'Zarina', 'Saparova', 'Astana', '+77011234581', 'Looking for elderly care specialist.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('timur.omarov@email.com', 'Timur', 'Omarov', 'Almaty', '+77011234582', 'Need someone to play with my children.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('aida.sultanova@email.com', 'Aida', 'Sultanova', 'Astana', '+77011234583', 'Seeking babysitter for my twin girls.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('yerlan.nazarov@email.com', 'Yerlan', 'Nazarov', 'Karaganda', '+77011234584', 'Need caregiver for elderly father.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('gulnara.tokayeva@email.com', 'Gulnara', 'Tokayeva', 'Astana', '+77011234585', 'Looking for afternoon playmate.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f'),
('serik.mustafin@email.com', 'Serik', 'Mustafin', 'Almaty', '+77011234586', 'Need reliable babysitter urgently.', 'scrypt:32768:8:1$VvXzK8LqRm2PjH8U$3a1d5f9e2b8c4a6d7f1e3b9a8c5d2f4e6a1c7b3d9e5f2a8b4c6d1e7f3a9b5c2d4e6f1a8b3c5d7e2f4a6b8c1d3e5f7a2b4c6d8e1f3a5b7c9d2e4f6a8b1c3d5e7f');

-- Insert Caregivers
INSERT INTO caregivers (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(1, 'sarah_photo.jpg', 'Female', 'Babysitter', 12.50),
(2, 'mike_photo.jpg', 'Male', 'Elderly Care', 15.00),
(3, 'emma_photo.jpg', 'Female', 'Playmate', 10.00),
(4, 'david_photo.jpg', 'Male', 'Babysitter', 11.00),
(5, 'lisa_photo.jpg', 'Female', 'Elderly Care', 16.50),
(6, 'john_photo.jpg', 'Male', 'Playmate', 9.50),
(7, 'anna_photo.jpg', 'Female', 'Babysitter', 13.00),
(8, 'robert_photo.jpg', 'Male', 'Elderly Care', 14.00),
(9, 'maria_photo.jpg', 'Female', 'Playmate', 8.50),
(10, 'james_photo.jpg', 'Male', 'Babysitter', 12.00);

-- Insert Members
INSERT INTO members (member_user_id, house_rules, dependent_description) VALUES
(11, 'No smoking. No pets.', '5-year-old son who likes painting and reading.'),
(12, 'Quiet environment preferred.', '82-year-old mother with limited mobility.'),
(13, 'Must be punctual. No pets.', '6-year-old daughter who loves outdoor activities.'),
(14, 'Non-smoker only.', '3-year-old twins, very energetic.'),
(15, 'Experience with dementia required. No pets.', '78-year-old grandmother with early-stage dementia.'),
(16, 'Pets friendly.', 'Two children aged 4 and 7, love playing games.'),
(17, 'Must follow strict schedule.', '8-month-old baby girl and 3-year-old boy.'),
(18, 'Medical background preferred.', '85-year-old father with diabetes.'),
(19, 'Outdoor play encouraged. No pets.', '5-year-old boy who loves sports.'),
(20, 'Must be reliable and on time.', '2-year-old daughter, very curious and active.');

-- Insert Addresses
INSERT INTO addresses (member_user_id, house_number, street, town) VALUES
(11, '15', 'Kabanbay Batyr', 'Esil District'),
(12, '42', 'Abay Avenue', 'Almaly District'),
(13, '7', 'Mangilik El', 'Esil District'),
(14, '88', 'Respublika Avenue', 'Central District'),
(15, '23', 'Syganak Street', 'Baykonur District'),
(16, '56', 'Dostyk Avenue', 'Medeu District'),
(17, '31', 'Turan Avenue', 'Esil District'),
(18, '99', 'Bukhar Zhyrau', 'Oktyabrsky District'),
(19, '12', 'Kabanbay Batyr', 'Saryarka District'),
(20, '67', 'Satpaev Street', 'Almaly District');

-- Insert Jobs
INSERT INTO jobs (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(11, 'Babysitter', 'Looking for patient and soft-spoken babysitter. Must have experience with young children.', '2024-11-01'),
(12, 'Elderly Care', 'Need someone with medical background. Soft-spoken preferred.', '2024-11-02'),
(13, 'Playmate', 'Active person needed for outdoor activities.', '2024-11-03'),
(14, 'Babysitter', 'Must be experienced with twins. Energy required!', '2024-11-04'),
(15, 'Elderly Care', 'Dementia care experience essential. Patient and soft-spoken.', '2024-11-05'),
(16, 'Playmate', 'Must love playing board games and outdoor sports.', '2024-11-06'),
(17, 'Babysitter', 'Need someone reliable for evening hours.', '2024-11-07'),
(18, 'Elderly Care', 'Diabetes management knowledge required.', '2024-11-08'),
(19, 'Playmate', 'Sports enthusiast preferred. Outdoor activities.', '2024-11-09'),
(20, 'Babysitter', 'Morning hours, must be punctual and soft-spoken.', '2024-11-10');

-- Insert Job Applications
INSERT INTO job_applications (caregiver_user_id, job_id, date_applied) VALUES
(1, 1, '2024-11-02'),
(4, 1, '2024-11-03'),
(7, 1, '2024-11-04'),
(2, 2, '2024-11-03'),
(5, 2, '2024-11-04'),
(3, 3, '2024-11-04'),
(6, 3, '2024-11-05'),
(1, 4, '2024-11-05'),
(10, 4, '2024-11-06'),
(8, 5, '2024-11-06'),
(9, 6, '2024-11-07'),
(3, 6, '2024-11-08'),
(7, 7, '2024-11-08'),
(2, 8, '2024-11-09'),
(5, 8, '2024-11-10');

-- Insert Appointments
INSERT INTO appointments (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(1, 11, '2024-11-15', '09:00:00', 4.0, 'accepted'),
(2, 12, '2024-11-16', '10:00:00', 6.0, 'accepted'),
(3, 13, '2024-11-17', '14:00:00', 3.0, 'accepted'),
(4, 14, '2024-11-18', '08:00:00', 5.0, 'pending'),
(5, 15, '2024-11-19', '11:00:00', 8.0, 'accepted'),
(6, 16, '2024-11-20', '15:00:00', 2.5, 'declined'),
(7, 17, '2024-11-21', '18:00:00', 4.0, 'accepted'),
(8, 18, '2024-11-22', '09:30:00', 7.0, 'accepted'),
(9, 19, '2024-11-23', '13:00:00', 3.5, 'pending'),
(10, 20, '2024-11-24', '07:00:00', 5.5, 'accepted'),
(1, 13, '2024-11-25', '10:00:00', 4.0, 'accepted');

-- End of database dump
