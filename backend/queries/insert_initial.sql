-- Teachers
INSERT INTO teachers (official_id, name, is_active) VALUES (1, 'Mosaddek Hossain Kamal Tushar', true);
SELECT * FROM teachers;

-- Courses
INSERT INTO courses (id, code, name, year, is_active, teacher_id) 
			VALUES  (1, 'CSE-3201', 'Operating System', 2023, true, 1);
SELECT * FROM courses;

-- Students
INSERT INTO students (id, student_card_id, registration_no, roll, name, is_active) 
			VALUES  (1, '04074b73606180', '2019-617-842', 59, 'Alve Reduan', true);

INSERT INTO students (id, student_card_id, registration_no, roll, name, is_active)
			VALUES  (2, '0470157A606180', '2019-617-XXX', 100, 'Test user', true);

SELECT * FROM students;


-- Devices
INSERT INTO devices (id, is_active) VALUES (1, true);
SELECT * FROM devices;

-- CourseDevices
INSERT INTO course_devices (id, course_id, device_id)
					VALUES (1, 1, 1);
SELECT * FROM course_devices;