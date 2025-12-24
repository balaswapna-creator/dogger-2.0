-- Fix Foreign Key Constraint to Allow CASCADE DELETE
-- Run this in PostgreSQL to fix the vaccination constraint

-- Step 1: Drop the old constraint
ALTER TABLE clinic_vaccination 
DROP CONSTRAINT IF EXISTS vaccinations_patient_id_32f70575_fk_patients_id;

-- Step 2: Add new constraint with CASCADE
ALTER TABLE clinic_vaccination 
ADD CONSTRAINT vaccinations_patient_id_32f70575_fk_patients_id 
FOREIGN KEY (patient_id) 
REFERENCES clinic_patients(id) 
ON DELETE CASCADE;

-- Verify the change
SELECT 
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    rc.delete_rule
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND tc.table_name = 'clinic_vaccination'
    AND kcu.column_name = 'patient_id';