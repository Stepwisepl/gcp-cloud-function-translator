# Google Cloud Function file translator

Cloud function sample for translating files stored in Cloud Storage.  
Flow looks like this:
1. Upload file with `to_translate` suffix to a bucket  
2. Cloud function receives event that file was upload and:
- reads file content
- translates to languages: {'PL', 'NO', 'ES', 'FR'}
- uploads translated file to same bucket