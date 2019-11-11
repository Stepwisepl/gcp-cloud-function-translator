from google.cloud import storage
from google.cloud import translate_v2

LANGUAGES_TRANSLATE_TO = {'PL', 'NO', 'ES', 'FR'}
TMP_INPUT_FILE = '/tmp/input_file'
TMP_OUTPUT_FILE = '/tmp/output_file'
FILE_SUFFIX_TO_TRANSLATE = 'to_translate'

storage_client = storage.Client()
translate_client = translate_v2.Client()


def translateFile(file_data, context):
    file_name: str = file_data['name']
    bucket_name = file_data['bucket']

    if not file_name.endswith(FILE_SUFFIX_TO_TRANSLATE):
        print(f'File not ending with "to_translate" [{file_name}], ignoring.')
        return

    bucket = storage_client.bucket(bucket_name)
    # download file to /tmp (the only dir we have access to on google cloud functions)
    bucket.blob(file_name).download_to_filename(TMP_INPUT_FILE)

    #read file content into input_str
    input_str = open(TMP_INPUT_FILE).read()

    #write translated output into local /tmp
    with open(TMP_OUTPUT_FILE, 'w') as file:
        file.write("%s\n" % f'EN(original):\n{input_str}')
        for language in LANGUAGES_TRANSLATE_TO:
            translated = translate_client.translate(
                input_str, target_language=language)
            file.write("%s\n" % f'{language}:\n{translated["translatedText"]}')

    # upload local output from /tmp into bucket
    output_file_name = f'{file_name.rpartition(FILE_SUFFIX_TO_TRANSLATE)[0]}_translated'
    bucket.blob(output_file_name).upload_from_filename(TMP_OUTPUT_FILE)


# for local dev purposes
# bucketTestData = {
#     "bucket":"gcp-cloud-function-translator",
#     "name":"test_to_translate"
# }
# translateFile(bucketTestData, None)