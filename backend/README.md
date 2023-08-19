To Run

```
bash
cd ..
uvicorn backend.main:app --reload
```

To update deployment
```
cd app/attendance/backend
git pull
pip3 install -r requirements.txt
sudo systemctl restart attendance
```