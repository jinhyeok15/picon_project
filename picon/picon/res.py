

def response_data(code, msg, **kwargs):
    data = {
        'statusCode': code,
        'responseMessage': msg,
    }
    for key, value in kwargs.items():
        data[key] = value
    return data


def error_data(e_res, **kwargs):
    for key, value in kwargs.items():
        e_res[key] = value
    return e_res


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
