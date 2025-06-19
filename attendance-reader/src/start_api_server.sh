#!/bin/bash
cd /home/pi/AttendanceManagementSystem/attendance-reader/src
/home/pi/.local/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
