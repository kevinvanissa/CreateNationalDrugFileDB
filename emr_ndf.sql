
/*
Comment 1: Change code that checks drug interaction to match new table
Comment 2: Change IndicationUsage 

*/

/*
create table Drug(
    drug_code varchar(11),
    drug_type_name varchar(100),
    primary key(drug_code)
);

create table Diagnosis(
    diagnosis_code varchar(11),
    diagnosis_name varchar(100),
    primary key(diagnosis_code)
);

create table DrugForm(
    form_code varchar(11),
    form_type_name varchar(100),
    primary key(form_code)
);


create table Interaction(
    interaction_code varchar(11),
    interaction_type_name varchar(100),
    primary key(interaction_code)
);


create table Ingredient(
    ingredient_code varchar(11),
    ingredient_type_name varchar(200),
    primary key(ingredient_code)
);


create table DrugInteraction(
    drug_code varchar(11),
    other_drug_code varchar(11),
    serverity varchar(20),
    primary key(drug_code,other_drug_code)
);



create table IndicationUsage(
    diagnosis_code varchar(11),
    drug_code varchar(11),
    primary key(diagnosis_code,drug_code),
    foreign key(diagnosis_code) references Diagnosis(diagnosis_code),
    foreign key(drug_code) references Drug(drug_code)
);

create table ContraIndication(
    diagnosis_code varchar(11),
    drug_code varchar(11),
    primary key(diagnosis_code,drug_code),
    foreign key(diagnosis_code) references Diagnosis(diagnosis_code),
    foreign key(drug_code) references Drug(drug_code)
);

create table IngredientInDrugs(
    ingredient_code varchar(11),
    drug_code varchar(11),
    primary key(ingredient_code,drug_code),
    foreign key(ingredient_code) references Ingredient(ingredient_code),
    foreign key(drug_code) references Drug(drug_code)
);

create table Patient(
    patient_ID varchar(8),
    fname varchar(30),
    lname varchar(30),
    dob date,
    sex varchar(10), 
    maritalStatus varchar (10), 
    bloodGroup varchar(4),
    primary key(patient_ID)
);

create table Patient_Diagnosis_log(
    patient_ID varchar(8),
    diagnosis_code varchar(11),
    is_current varchar(3),
    diagnosis_date datetime,
    recovery_date datetime,
    primary key(patient_ID,diagnosis_code,diagnosis_date),
    foreign key(patient_ID) references Patient(patient_ID),
    foreign key(diagnosis_code) references Diagnosis(diagnosis_code)
);

create table Patient_Medication_log(
    patient_ID varchar(8),
    drug_code varchar(11),
    is_current varchar(3),
    medication_start_date datetime,
    medication_end_date datetime,
    primary key(patient_ID,drug_code,medication_start_date),
    foreign key(patient_ID) references Patient(patient_ID),
    foreign key(drug_code) references Drug(drug_code)
);

create table Patient_Allergies_log(
    patient_ID varchar(8),
    drug_code varchar(11),
    primary key(patient_ID,drug_code),
    foreign key(patient_ID) references Patient(patient_ID),
    foreign key(drug_code) references Drug(drug_code)
);


create table MechanismAction(
    mechanism_code varchar(11),
    mechanism_type_name varchar(200),
    primary key(mechanism_code)
);


create table PharmacoKinetics(
    pharmaco_code varchar(11),
    pharmaco_type_name varchar(200),
    primary key(pharmaco_code)
);

create table PhysiologicEffect(
    physiologic_code varchar(11),
    physiologic_type_name varchar(200),
    primary key(physiologic_code)
);

create table TherapeuticCategory(
    therapeutic_code varchar(11),
    therapeutic_type_name varchar(200),
    primary key(therapeutic_code)
);

create table MechanismActionInDrugs(
    mechanism_code varchar(11),
    drug_code varchar(11),
    primary key(mechanism_code,drug_code),
    foreign key(mechanism_code) references MechanismAction(mechanism_code),
    foreign key(drug_code) references Drug(drug_code)
);

create table PharmacoKineticsInDrugs(
    pharmaco_code varchar(11),
    drug_code varchar(11),
    primary key(pharmaco_code,drug_code),
    foreign key(pharmaco_code) references PharmacoKinetics(pharmaco_code),
    foreign key(drug_code) references Drug(drug_code)
);

create table PhysiologicEffectInDrugs(
    physiologic_code varchar(11),
    drug_code varchar(11),
    primary key(physiologic_code,drug_code),
    foreign key(physiologic_code) references PhysiologicEffect(physiologic_code),
    foreign key(drug_code) references Drug(drug_code)
);

create table TherapeuticCategoryInDrugs(
    therapeutic_code varchar(11),
    drug_code varchar(11),
    primary key(therapeutic_code,drug_code),
    foreign key(therapeutic_code) references TherapeuticCategory(therapeutic_code),
    foreign key(drug_code) references Drug(drug_code)
);
*/

/*============================INSERTS===========================*/

/*
insert into Patient values ('P001','Dundee','Miller','2012-08-15','Male','Married','O');
insert into Patient values ('P002','John','Brown','2013-01-16','Male','Single','A');
insert into Patient values ('P003','Stacy','Walters','2012-11-02','Female','Single','AB');
insert into Patient values ('P004','Robert','Johnson','1978-11-02','Male','Married','O');
insert into Patient values ('P005','Judge','Burke','1960-11-02','Male','Married','B');
insert into Patient values ('P006','Fenton','Ferguson','1970-11-02','Male','Single','AB');
insert into Patient values ('P007','Stacy','Scarlett','1977-05-02','Female','Married','O');
insert into Patient values ('P008','Annett','Wilks','1969-12-02','Female','Married','AB');


insert into Patient_Diagnosis_log (patient_ID,diagnosis_code,is_current,diagnosis_date) values
('P001','N0000001616','YES','2010-12-01 00:00:00');

insert into Patient_Diagnosis_log (patient_ID,diagnosis_code,is_current,diagnosis_date) values
('P002','N0000000950','YES','2008-12-01 00:00:00');


insert into Patient_Medication_log (patient_ID,drug_code,is_current,medication_start_date) values
('P001','N0000146784','YES','2014-01-01 00:00:00');

insert into Patient_Medication_log (patient_ID,drug_code,is_current,medication_start_date) values
('P002','N0000145957','YES','2014-01-01 00:00:00');


insert into Patient_Allergies_log values
('P001','N0000152547');

insert into Patient_Allergies_log values
('P001','N0000020300');

insert into Patient_Allergies_log values
('P001','N0000147169');

*/
