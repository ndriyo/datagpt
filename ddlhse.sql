CREATE TABLE [dbo].[Doctor_Schedule_Changes] (
    [change_id] int NOT NULL,
    [doctor_id] int NOT NULL,
    [hospital_id] int NOT NULL,
    [location_id] int NOT NULL,
    [change_type] nvarchar(40) NOT NULL,
    [change_reason] nvarchar(200) NULL,
    [start_date] date NOT NULL,
    [end_date] date NOT NULL,
    [start_time] time NOT NULL,
    [end_time] time NOT NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL
);


CREATE TABLE [dbo].[Doctor_Schedules] (
    [schedule_id] int NOT NULL,
    [doctor_id] int NOT NULL,
    [hospital_id] int NOT NULL,
    [location_id] int NOT NULL,
    [day_of_week] nvarchar(20) NOT NULL,
    [start_time] time NOT NULL,
    [end_time] time NOT NULL,
    [max_slot] int NOT NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL
);


CREATE TABLE [dbo].[Doctor_Specializations] (
    [specialization_id] int NOT NULL,
    [hospital_id] int NOT NULL,
    [location_id] int NOT NULL,
    [specialization] nvarchar(200) NOT NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL
);


CREATE TABLE [dbo].[Doctors] (
    [doctor_id] int NOT NULL,
    [first_name] nvarchar(100) NOT NULL,
    [last_name] nvarchar(100) NOT NULL,
    [specialization_id] int NOT NULL,
    [contact_info] nvarchar(200) NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL,
    [title] nvarchar(200) NOT NULL,
    [qualification] nvarchar(200) NOT NULL,
    [sub_specialization] nvarchar(100) NULL,
    [sub_spec_exclusivity] nvarchar(20) NULL,
    [initial] nvarchar(20) NULL
);


CREATE TABLE [dbo].[Hospital_Locations] (
    [location_id] int NOT NULL,
    [hospital_id] int NOT NULL,
    [location_name] nvarchar(200) NOT NULL,
    [address] nvarchar(400) NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL,
    [code] nvarchar(40) NULL
);


CREATE TABLE [dbo].[Hospitals] (
    [hospital_id] int NOT NULL,
    [hospital_name] nvarchar(200) NOT NULL,
    [contact_info] nvarchar(200) NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL
);


CREATE TABLE [dbo].[Outpatient_Registrations] (
    [registration_id] int NOT NULL,
    [patient_id] int NOT NULL,
    [doctor_id] int NOT NULL,
    [hospital_id] int NOT NULL,
    [location_id] int NOT NULL,
    [visit_date] date NOT NULL,
    [visit_time] time NOT NULL,
    [symptoms] nvarchar(MAX) NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL
);


CREATE TABLE [dbo].[Patients] (
    [patient_id] int NOT NULL,
    [first_name] nvarchar(100) NOT NULL,
    [last_name] nvarchar(100) NOT NULL,
    [gender] char(1) NOT NULL,
    [date_of_birth] date NOT NULL,
    [address] nvarchar(400) NULL,
    [ktp] char(16) NULL,
    [related_patient_id] int NULL,
    [relation_type] nvarchar(40) NULL,
    [hospital_id] int NOT NULL,
    [location_id] int NOT NULL,
    [created_by] nvarchar(100) NULL,
    [created_date] datetime NULL,
    [last_updated_by] nvarchar(100) NULL,
    [last_updated_date] datetime NULL,
    [nrm] nvarchar(40) NULL,
    [phone_number] nvarchar(40) NULL
);

ALTER TABLE [dbo].[Doctor_Schedule_Changes] ADD CONSTRAINT [FK_Doctor_Schedule_Changes_Doctors] FOREIGN KEY ([doctor_id]) REFERENCES [dbo].[Doctors] ([doctor_id]);

ALTER TABLE [dbo].[Doctor_Schedule_Changes] ADD CONSTRAINT [FK_Doctor_Schedule_Changes_Hospitals] FOREIGN KEY ([hospital_id]) REFERENCES [dbo].[Hospitals] ([hospital_id]);

ALTER TABLE [dbo].[Doctor_Schedule_Changes] ADD CONSTRAINT [FK_Doctor_Schedule_Changes_Locations] FOREIGN KEY ([location_id]) REFERENCES [dbo].[Hospital_Locations] ([location_id]);

ALTER TABLE [dbo].[Doctor_Schedules] ADD CONSTRAINT [FK_Doctor_Schedules_Doctors] FOREIGN KEY ([doctor_id]) REFERENCES [dbo].[Doctors] ([doctor_id]);

ALTER TABLE [dbo].[Doctor_Schedules] ADD CONSTRAINT [FK_Doctor_Schedules_Hospital_Locations] FOREIGN KEY ([location_id]) REFERENCES [dbo].[Hospital_Locations] ([location_id]);

ALTER TABLE [dbo].[Doctor_Schedules] ADD CONSTRAINT [FK_Doctor_Schedules_Hospitals] FOREIGN KEY ([hospital_id]) REFERENCES [dbo].[Hospitals] ([hospital_id]);

ALTER TABLE [dbo].[Doctor_Specializations] ADD CONSTRAINT [FK_DoctorSpecializations_Hospitals] FOREIGN KEY ([hospital_id]) REFERENCES [dbo].[Hospitals] ([hospital_id]);

ALTER TABLE [dbo].[Doctor_Specializations] ADD CONSTRAINT [FK_DoctorSpecializations_Locations] FOREIGN KEY ([location_id]) REFERENCES [dbo].[Hospital_Locations] ([location_id]);

ALTER TABLE [dbo].[Doctors] ADD CONSTRAINT [FK_Doctors_Specializations] FOREIGN KEY ([specialization_id]) REFERENCES [dbo].[Doctor_Specializations] ([specialization_id]);

ALTER TABLE [dbo].[Hospital_Locations] ADD CONSTRAINT [FK_Hospital_Locations_Hospitals] FOREIGN KEY ([hospital_id]) REFERENCES [dbo].[Hospitals] ([hospital_id]);

ALTER TABLE [dbo].[Outpatient_Registrations] ADD CONSTRAINT [FK_Outpatient_Doctor] FOREIGN KEY ([doctor_id]) REFERENCES [dbo].[Doctors] ([doctor_id]);

ALTER TABLE [dbo].[Outpatient_Registrations] ADD CONSTRAINT [FK_Outpatient_Hospital_Locations] FOREIGN KEY ([location_id]) REFERENCES [dbo].[Hospital_Locations] ([location_id]);

ALTER TABLE [dbo].[Outpatient_Registrations] ADD CONSTRAINT [FK_Outpatient_Hospitals] FOREIGN KEY ([hospital_id]) REFERENCES [dbo].[Hospitals] ([hospital_id]);

ALTER TABLE [dbo].[Outpatient_Registrations] ADD CONSTRAINT [FK_Outpatient_Patient] FOREIGN KEY ([patient_id]) REFERENCES [dbo].[Patients] ([patient_id]);

ALTER TABLE [dbo].[Patients] ADD CONSTRAINT [FK_Patients_Hospital_Locations] FOREIGN KEY ([location_id]) REFERENCES [dbo].[Hospital_Locations] ([location_id]);

ALTER TABLE [dbo].[Patients] ADD CONSTRAINT [FK_Patients_Hospitals] FOREIGN KEY ([hospital_id]) REFERENCES [dbo].[Hospitals] ([hospital_id]);

ALTER TABLE [dbo].[Patients] ADD CONSTRAINT [FK_Patients_Related_Patient] FOREIGN KEY ([related_patient_id]) REFERENCES [dbo].[Patients] ([patient_id]);

CREATE TABLE [dbo].[Queue_Transactions] (
    [queue_id]        INT           IDENTITY(1,1) NOT NULL,
    [registration_id] INT           NULL,  -- link ke Outpatient_Registrations (jika antrian dokter)
    [patient_id]      INT           NOT NULL,
    [hospital_id]     INT           NOT NULL,
    [location_id]     INT           NOT NULL,
    [doctor_id]       INT           NULL,  -- terisi jika service_type = 'DOCTOR'
    [service_type]    NVARCHAR(20)  NOT NULL,  -- misal: 'DOCTOR', 'LAB', 'CASHIER', 'PHARMACY', dll.
    [queue_date]      DATE          NOT NULL,   -- untuk reset nomor harian
    [sequence_no]     INT           NOT NULL,   -- nomor urut harian
    [queue_number]    NVARCHAR(20)  NOT NULL,   -- format antrian final (e.g. DERA001, LAB003, ...)
    [status]          NVARCHAR(20)  NOT NULL,   -- waiting, in_progress, done, canceled
    [created_by]      NVARCHAR(100) NULL,
    [created_date]    DATETIME      NOT NULL DEFAULT (GETDATE()),
    [last_updated_by] NVARCHAR(100) NULL,
    [last_updated_date] DATETIME    NULL,

    CONSTRAINT [PK_Queue_Transactions] PRIMARY KEY CLUSTERED ([queue_id] ASC)
);

ALTER TABLE [dbo].[Queue_Transactions]
ADD CONSTRAINT [FK_Queue_Transactions_Registration]
    FOREIGN KEY ([registration_id]) REFERENCES [dbo].[Outpatient_Registrations]([registration_id]);

ALTER TABLE [dbo].[Queue_Transactions]
ADD CONSTRAINT [FK_Queue_Transactions_Patient]
    FOREIGN KEY ([patient_id]) REFERENCES [dbo].[Patients]([patient_id]);

ALTER TABLE [dbo].[Queue_Transactions]
ADD CONSTRAINT [FK_Queue_Transactions_Hospital]
    FOREIGN KEY ([hospital_id]) REFERENCES [dbo].[Hospitals]([hospital_id]);

ALTER TABLE [dbo].[Queue_Transactions]
ADD CONSTRAINT [FK_Queue_Transactions_Location]
    FOREIGN KEY ([location_id]) REFERENCES [dbo].[Hospital_Locations]([location_id]);

ALTER TABLE [dbo].[Queue_Transactions]
ADD CONSTRAINT [FK_Queue_Transactions_Doctor]
    FOREIGN KEY ([doctor_id]) REFERENCES [dbo].[Doctors]([doctor_id]);
