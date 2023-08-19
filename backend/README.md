To Run

```
bash
cd ..
uvicorn backend.main:app --reload
```

To update deployment
```
git pull
sudo systemctl restart attendance
```