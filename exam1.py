
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Patient(BaseModel):
    id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    is_available: bool = True

class Appointment(BaseModel):
    id: int
    patient: Patient
    doctor: Doctor
    date: str


patients: List[Patient] = []
doctors: List[Doctor] = []
appointments: List[Appointment] = []


@app.post("/patients")
async def create_patient(patient: Patient):
    patients.append(patient)
    return patient

@app.get("/patients")
async def read_patients():
    return patients

@app.get("/patients/{patient_id}")
async def read_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    

@app.put("/patients/{patient_id}")
async def update_patient(patient_id: int, patient: Patient):
    for p in patients:
        if p.id == patient_id:
            p.name = patient.name
            p.age = patient.age
            p.sex = patient.sex
            p.weight = patient.weight
            p.height = patient.height
            p.phone = patient.phone
            return p



@app.post("/doctors")
async def create_doctor(doctor: Doctor):
    doctors.append(doctor)
    return doctor

@app.get("/doctors")
async def read_doctors():
    return doctors

@app.get("/doctors/{doctor_id}")
async def read_doctor(doctor_id: int):
    for doctor in doctors:
        if doctor.id == doctor_id:
            return doctor
   

@app.put("/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, doctor: Doctor):
    for d in doctors:
        if d.id == doctor_id:
            d.name = doctor.name
            d.specialization = doctor.specialization
            d.phone = doctor.phone
            d.is_available = doctor.is_available
            return d
    

@app.delete("/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int):
    for doctor in doctors:
        if doctor.id == doctor_id:
            doctors.remove(doctor)
            return

@app.put("/doctors/{doctor_id}/availability")
async def set_availability(doctor_id: int, is_available: bool):
    for doctor in doctors:
        if doctor.id == doctor_id:
            doctor.is_available = is_available
            return doctor
    
   
@app.post("/appointments")
async def create_appointment(patient_id: int):
    patient = next((p for p in patients if p.id == patient_id), None)
    if patient is None:
        raise HTTPException(status_code=404)
    available_doctors = [d for d in doctors if d.is_available]
    if not available_doctors:
        raise HTTPException(status_code=503, detail="No doctors available")
    doctor = available_doctors[0]
    appointment = Appointment(id=len(appointments) + 1, patient=patient, doctor=doctor, date="2024-05-03")
    appointments.append(appointment)
    doctor.is_available = False
    return appointment


@app.put("/appointments/{appointment_id}/complete")
async def complete_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment.id == appointment_id:
            appointment.doctor.is_available = True
            return appointment

