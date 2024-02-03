# File Uploader API

via Django REST Framework and Celery

---

## Endpoints

### [GET] api/files/

Returns all files from DB like:
```
[
    {
        "id": int,
        "file": http://localhost:2727/path/to/file/on/server,
        "uploaded_at": datetime,
        "processed": whether file was processed or not,
        "data": {
            "size": file size,
            "filename": file name,
            "extension": file extension,
            <file_specific_data>
        }
    },
    ...
]
```

### [POST] api/upload/

Upload files with form-data body.

- key: files
- value: file(s)_to_upload
