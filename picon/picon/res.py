

def response_data(code, msg, **kwargs):
    data = {
        'statusCode': code,
        'responseMessage': msg,
    }
    for key, value in kwargs.items():
        data[key] = value
    return data


def error_data(code, msg, e_res, **kwargs):
    data = {
        'statusCode': code,
        'responseMessage': msg,
    }
    data.update(e_res)
    for key, value in kwargs.items():
        data[key] = value
    return data


# 200
OK = '조회성공'

# 201
CREATED = '생성완료'
UPDATED = '수정완료'

# 204
DELETED = '삭제완료'

# 400
NOT_EXIST_USER = '존재하지 않는 유저입니다.'
SAME_ID = '본인을 팔로우할 수 없습니다.'
NOT_VALID = '유효하지 않은 데이터입니다.'

# 403
UPLOAD_ERROR = '업로드를 할 수 없습니다.'

# 404
DOES_NOT_EXIST = '해당 객체가 존재하지 않습니다.'
NOT_MATCH_WITH_DB = 'Request body is not match with DB, please check your body'
