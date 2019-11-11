from google.cloud import storage
from google.cloud import translate_v2


LANGUAGES_TO_TRANSLATE = {'PL', 'NO', 'ES', 'FR'}
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
    bucket.blob(file_name).download_to_filename(TMP_INPUT_FILE)

    input_str = open(TMP_INPUT_FILE).read()

    target_languages = LANGUAGES_TO_TRANSLATE

    with open(TMP_OUTPUT_FILE, 'w') as file:
        file.write("%s\n" % f'EN(original):\n{input_str}')
        for language in target_languages:
            translated = translate_client.translate(
                input_str, target_language=language)
            file.write("%s\n" % f'{language}:\n{translated["translatedText"]}')

    output_file_name = f'{file_name.rpartition(FILE_SUFFIX_TO_TRANSLATE)[0]}_translated'
    bucket.blob(output_file_name).upload_from_filename(TMP_OUTPUT_FILE)


# for local dev purposes
# bucketTestData = {
#     "bucket":"gcp-cloud-function-translator",
#     "name":"test_to_translate"
# }
# translateFile(bucketTestData, None)