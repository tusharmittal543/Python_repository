from ast import main
from typing import Optional

import app
from fastapi import HTTPException
from fastapi import Response


@app.get("/attendence_log")
def attendence_log(
    id: Optional[str] = None,
    student_id: Optional[str] = None,
    course_id: Optional[str] = None,
    present: Optional[str] = None,
    submitted_by: Optional[str] = None,
    updated_at: Optional[str] = None

    ):
 if not id or not student_id:
    raise HTTPException(status_code=400, detail="Both 'id' and 'student_id' parameters are required.")

 @app.get("/coursed")
 def coursed(
    id: Optional[str] = None,
    course_name: Optional[str] = None,
    department_id: Optional[str] = None,
    semester: Optional[str] = None,
    className: Optional[str] = None,
    lectures_hours: Optional[str] = None,
    submitted_by: Optional[str] = None,
    updated_at: Optional[str] = None
 ):

  if not id or not department_id:
    raise HTTPException(status_code=400, detail="Both 'id' and 'department_id' parameters are required.")


@app.get("/users")
def users(
             id: Optional[str] = None,
             type: Optional[str] = None,
             full_name: Optional[str] = None,
             username: Optional[str] = None,
             email: Optional[str] = None,
             password: Optional[str] = None,
             submitted_by: Optional[str] = None,
             updated_at: Optional[str] = None

        ):

    if not id :
            raise HTTPException(status_code=400, detail="Id parameters is required.")

    @app.get("/departments")
    def departments(
             id: Optional[str] = None,
             department_name: Optional[str] = None,
             submitted_by: Optional[str] = None,
             updated_at: Optional[str] = None


      ):

      if not id:
       raise HTTPException(status_code=400, detail="Id parameters is required.")

@app.get("/students")
def students(
             id: Optional[str] = None,
             full_name: Optional[str] = None,
             department_id: Optional[str] = None,
             className: Optional[str] = None,
            submitted_by: Optional[str] = None,
            updated_at: Optional[str] = None


     ):

 if not id:
  raise HTTPException(status_code=400, detail="Id parameters is required.")

if __name__ == "__main__":
      main()








